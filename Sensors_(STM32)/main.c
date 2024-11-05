/* Includes ------------------------------------------------------------------*/ 
#include "main.h" 
#include "stm32f1xx_hal.h" 
#include "usb_device.h" 
/* USER CODE BEGIN Includes */ 
#include "usbd_cdc_if.h" 
#include "string.h" 
#include "math.h" 
#include "mpu6050.h" 
/* USER CODE END Includes */ 
/* Private variables ---------------------------------------------------------*/ 
ADC_HandleTypeDef hadc1; 
I2C_HandleTypeDef hi2c2; 
UART_HandleTypeDef huart1; 
/* USER CODE BEGIN PV */ 
/* Private variables ---------------------------------------------------------*/ 
MPU6050_t MPU6050; 
char buf[16]; 
int uart_buf_len; 
float x; 
int duration = 50; 
int motor_pos_1 = 0; 
int motor_pos_2 = 0; 
int motor_pos_3 = 0; 
int motor_pos_4 = 0; 
float currentTime = 0;  
float previousTime = 0; 
float pi = 22/7; 
float wheel_radius = 40; 
float rpm_1 = 0; 
float rpm_2 = 0; 
float rpm_3 = 0; 
float rpm_4 = 0; 
float v_x = 0; 
float v_y = 0; 
float Ax =  0; 
float Ay =  0; 
int ppr = 330;  
float adc = 0; 
float voltage = 0; 
int battery = 0; 
/* USER CODE END PV */ 
/* Private function prototypes -----------------------------------------------*/ 
void SystemClock_Config(void); 
static void MX_GPIO_Init(void); 
static void MX_USART1_UART_Init(void); 
static void MX_I2C2_Init(void); 
 
static void MX_ADC1_Init(void); 
 
/* USER CODE BEGIN PFP */ 
/* Private function prototypes -----------------------------------------------*/ 
int battery_checker(float battery_voltage) { 
 int battery_perc; 
  if (battery_voltage <= 3.1 && battery_voltage > 3.05) {battery_perc = 100;} 
  else if (battery_voltage <= 3.05 && battery_voltage > 3) {battery_perc = 90;} 
  else if (battery_voltage <= 3 && battery_voltage > 2.95) {battery_perc = 80;} 
  else if (battery_voltage <= 2.95 && battery_voltage > 2.9) {battery_perc = 70;} 
  else if (battery_voltage <= 2.9 && battery_voltage > 2.85) {battery_perc = 60;} 
  else if (battery_voltage <= 2.85 && battery_voltage > 2.8) {battery_perc = 50;} 
  else if (battery_voltage <= 2.8 && battery_voltage > 2.75) {battery_perc = 40;} 
  else if (battery_voltage <= 2.75 && battery_voltage > 2.7) {battery_perc = 30;} 
  else if (battery_voltage <= 2.7) {battery_perc = 20;} 
 return battery_perc; 
} 
/* USER CODE END PFP */ 
 
/* USER CODE BEGIN 0 */ 
 
/* USER CODE END 0 */ 
 
int main(void) 
{ 
  /* USER CODE BEGIN 1 */ 
 
  /* USER CODE END 1 */ 
 
  /* MCU Configuration----------------------------------------------------------*/ 
 
  /* Reset of all peripherals, Initializes the Flash interface and the 
Systick. */ 
  HAL_Init(); 
 
  /* USER CODE BEGIN Init */ 
 
  /* USER CODE END Init */ 
 
  /* Configure the system clock */ 
  SystemClock_Config(); 
 
  /* USER CODE BEGIN SysInit */ 
 
  /* USER CODE END SysInit */ 
 
  /* Initialize all configured peripherals */ 
  MX_GPIO_Init(); 
  MX_USB_DEVICE_Init(); 
  MX_USART1_UART_Init(); 
  MX_I2C2_Init(); 
 
  MX_ADC1_Init(); 
 
  /* USER CODE BEGIN 2 */ 
  while (MPU6050_Init(&hi2c2) == 1){}; 
  MPU6050_Init(&hi2c2); 
  HAL_ADCEx_Calibration_Start(&hadc1); 
  /* USER CODE END 2 */ 
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET); 
  /* Infinite loop */ 
  /* USER CODE BEGIN WHILE */ 
  while (1) 
  { 
  /* USER CODE END WHILE */ 
    MPU6050_Read_All(&hi2c2, &MPU6050); 
      
    HAL_ADC_Start(&hadc1); 
    HAL_ADC_PollForConversion(&hadc1, 100); 
    adc = (float)(HAL_ADC_GetValue(&hadc1)); 
    voltage = adc/4096*3.3;  
    battery = (int)(battery_checker(voltage)); 
    HAL_ADC_Stop(&hadc1); 
      
    currentTime = HAL_GetTick();  

    if (currentTime - previousTime > duration)
    { 
      __disable_irq(); 
      previousTime = currentTime; 
        
      rpm_1 = (float)motor_pos_1/(float)ppr*(float)(60000/duration);  
      rpm_2 = (float)motor_pos_2/(float)ppr*(float)(60000/duration);  
      rpm_3 = (float)motor_pos_3/(float)ppr*(float)(60000/duration);  
      rpm_4 = (float)motor_pos_4/(float)ppr*(float)(60000/duration);  
      
      //v_x = (wheel_radius/4)*(rpm_1 + rpm_2 + rpm_3 + rpm_4); 
      //v_y = (wheel_radius/4)*((-rpm_1) + rpm_2 + rpm_3 + rpm_4); 
      
      v_x = (wheel_radius/4)*(rpm_2 + rpm_4 + rpm_1 + rpm_3); 
      v_y = (wheel_radius/4)*((-rpm_2) + rpm_4 + rpm_1 - rpm_3); 
      
      motor_pos_1 = 0; 
      motor_pos_2 = 0; 
      motor_pos_3 = 0; 
      motor_pos_4 = 0; 
    } 
    __enable_irq (); 
    Ax = MPU6050.Ax; 
    Ay = MPU6050.Ay;  
    uart_buf_len = sprintf(buf, "%f,%f,%f,%f,%f,%f,%d\n", rpm_1, 
    rpm_2, rpm_3, rpm_4, Ax, Ay, battery); 
    v_x = 0; 
    v_y = 0; 
    CDC_Transmit_FS((uint8_t *)buf, uart_buf_len); 
    HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13); 
      
    HAL_Delay(50); 
  } 
} 

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) 
{ 
  if(GPIO_Pin == GPIO_PIN_5)  
  { 
    if(HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_4)) {motor_pos_1 += 1;} 
  else {motor_pos_1 -= 1;}  
  }  
  else if(GPIO_Pin == GPIO_PIN_9)  
  { 
    if(HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_8)) {motor_pos_2 += 1;} 
  else {motor_pos_2 -= 1;} 
  }  
  else if(GPIO_Pin == GPIO_PIN_12)  
  { 
    if(HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_13)) {motor_pos_3 += 1;} 
  else {motor_pos_3 -= 1;} 
  } 
  else if(GPIO_Pin == GPIO_PIN_15)  
  { 
    if(HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_3)) {motor_pos_4 += 1;} 
  else {motor_pos_4 -= 1;} 
  } 
}