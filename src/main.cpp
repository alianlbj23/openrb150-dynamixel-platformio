#include <Arduino.h>
#include <micro_ros_platformio.h>

#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <rmw_microros/rmw_microros.h>

#include <std_msgs/msg/float32.h>
#include <std_msgs/msg/bool.h>

// 資源宣告
rcl_publisher_t state_pub;
rcl_subscription_t led_sub;
std_msgs__msg__Float32 state_msg;
std_msgs__msg__Bool led_msg;

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

float current_angle = 0.0; // 模擬你的角度數據
#define LED_PIN LED_BUILTIN

// --- Subscribe Callback: 控制 LED ---
void led_sub_callback(const void * msgin) {
  const std_msgs__msg__Bool * msg = (const std_msgs__msg__Bool *)msgin;
  digitalWrite(LED_PIN, msg->data ? HIGH : LOW);
}

// --- Timer Callback: 定時發佈角度 (參考你的修正) ---
void pub_timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)timer; 
  (void)last_call_time;

  // 更新數據並發佈
  state_msg.data = current_angle;
  rcl_publish(&state_pub, &state_msg, NULL);
  
  // 同步 Session 確保連線健康 (你提供的關鍵修正)
  (void)rmw_uros_sync_session(100);

  // 測試用：讓數值變動
  current_angle += 1.0;
  if (current_angle > 360.0) current_angle = 0.0;
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  
  // micro-ROS 傳輸設定
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();

  // 等待 Agent 連線
  while (RMW_RET_OK != rmw_uros_ping_agent(100, 10)) {
    delay(100);
  }

  // 初始化 rclc
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "openrb_node", "", &support);

  // 初始化 Publisher (發佈角度)
  rclc_publisher_init_default(
    &state_pub,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
    "/current_angle");

  // 初始化 Subscription (接收 LED 指令)
  rclc_subscription_init_default(
    &led_sub,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),
    "/led_control");

  // 初始化 Timer (設定為 50ms)
  rclc_timer_init_default(
    &timer,
    &support,
    RCL_MS_TO_NS(50),
    pub_timer_callback);

  // 初始化 Executor (Handles: 1 Timer + 1 Subscription = 2)
  executor = rclc_executor_get_zero_initialized_executor();
  rclc_executor_init(&executor, &support.context, 2, &allocator);
  rclc_executor_add_timer(&executor, &timer);
  rclc_executor_add_subscription(&executor, &led_sub, &led_msg, &led_sub_callback, ON_NEW_DATA);
}

void loop() {
  // 保持執行
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(10));
}