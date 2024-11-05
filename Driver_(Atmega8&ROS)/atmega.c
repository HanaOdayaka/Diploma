#include <avr/io.h> 
#include <avr/interrupt.h> 
#define F_CPU 500000UL  
#define LEN 32   
#include <util/delay.h>  
#include <stdio.h> 
#include <string.h> 
#include <stdlib.h> 
 
#define MOTOR_PB     1 
#define MOTOR_PWM    OCR1A      
#define MOTOR_PB_2   3 
#define MOTOR_PWM_2  OCR2   
 
char data[LEN]; 
register unsigned char IT asm("r16"); 
int i; 
int lng; 
int pwm; 
char myst[35]; 
char* mystr = myst; 
char rc; 
const unsigned char MAX_STRING = 30;  
volatile unsigned char IDX; 
volatile unsigned char done; 
 
//Остановка 
void stop() 
{ 
   //светодиод 
   PORTB &= ~( 1 << PB6 );  
  
   //левый передний мотор 
   PORTC |=  ( 1 << PC3 ); 
   PORTC |=  ( 1 << PC2 );  

   //левый задний мотор 
   PORTC |=  ( 1 << PC4 ); 
   PORTC |=  ( 1 << PC5 );  

   //правый передний мотор  
   PORTD |=  ( 1 << PD7 ); 
   PORTB |=  ( 1 << PB0 ); 

   //правый задний мотор 
   PORTD |=  ( 1 << PD6 ); 
   PORTB |=  ( 1 << PB2 );  

   //вывод сообщения 
   //mystr = "stop"; 
   //UART_message(lng, mystr); 
  
} 
 
//Движение вперед 
void forward() 
{ 
   //светодиод 
   PORTB |=  ( 1 << PB6 );  
 
   //левый передний мотор 
   PORTC |=  ( 1 << PC3 ); 
   PORTC &= ~( 1 << PC2 );  

   //левый задний мотор 
   PORTC |=  ( 1 << PC4 ); 
   PORTC &= ~( 1 << PC5 );  

   //правый передний мотор 
   PORTD |=  ( 1 << PD7 ); 
   PORTB &= ~( 1 << PB0 );  

   //правый задний мотор 
   PORTD |=  ( 1 << PD6 ); 
   PORTB &= ~( 1 << PB2 );  

   //вывод сообщения 
   //mystr = "forward"; 
   //UART_message(lng, mystr);   
} 
 
//Движение назад 
void backward() 
{ 
   //светодиод 
   PORTC |=  ( 1 << PB6 );   
 
   //левый передний мотор 
   PORTC &= ~( 1 << PC3 ); 
   PORTC |=  ( 1 << PC2 );  

   //левый задний мотор 
   PORTC &= ~( 1 << PC4 ); 
   PORTC |=  ( 1 << PC5 );  

   //правый передний мотор  
   PORTD &= ~( 1 << PD7 ); 
   PORTB |=  ( 1 << PB0 ); 

   //правый задний мотор 
   PORTD &= ~( 1 << PD6 ); 
   PORTB |=  ( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "backward"; 
   //UART_message(lng, mystr);  
} 
 
//Движение вправо 
void right() 
{ 
   //светодиод 
   PORTB |=  ( 1 << PB6 ); 
   
   //левый передний мотор 
   PORTC |=  ( 1 << PC3 ); 
   PORTC &= ~( 1 << PC2 );  

   //левый задний мотор 
   PORTC &= ~( 1 << PC4 ); 

   PORTC |=  ( 1 << PC5 );  

   //правый передний мотор 
   PORTD &= ~( 1 << PD7 ); 
   PORTB |=  ( 1 << PB0 );  

   //правый задний мотор 
   PORTD |=  ( 1 << PD6 ); 
   PORTB &= ~( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "moving to the right"; 
   //UART_message(lng, mystr);  
} 
 
 
//Движение влево 
void left() 
{ 
 //светодиод 
    PORTB |=  ( 1 << PB6 ); 
   
   //левый передний мотор 
   PORTC &= ~( 1 << PC3 ); 
   PORTC |=  ( 1 << PC2 );  

   //левый задний мотор 
   PORTC |=  ( 1 << PC4 ); 
   PORTC &= ~( 1 << PC5 );  

   //правый передний мотор 
   PORTD |=  ( 1 << PD7 ); 
   PORTB &= ~( 1 << PB0 );  

   //правый задний мотор 
   PORTD &= ~( 1 << PD6 ); 
   PORTB |=  ( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "moving to the left"; 
   //UART_message(lng, mystr);  
} 
 
//Движение вправо вверх по диагонали 
void right_up_diagonal() 
{ 
 //светодиод 
   PORTB |=  ( 1 << PB6 ); 
   
   //левый передний мотор 
   PORTC |=  ( 1 << PC3 ); 
   PORTC &= ~( 1 << PC2 );  

   //левый задний мотор 
   PORTC &= ~( 1 << PC4 ); 
   PORTC &= ~( 1 << PC5 );  

   //правый передний мотор 
   PORTD &= ~( 1 << PD7 ); 
   PORTB &= ~( 1 << PB0 );  


   //правый задний мотор 
   PORTD |=  ( 1 << PD6 ); 
   PORTB &= ~( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "moving diagonally to the right up"; 
   //UART_message(lng, mystr);  
} 
 
//Движение влево вверх по диагонали 
void left_up_diagonal() 
{ 
 //светодиод 
   PORTB |=  ( 1 << PB6 ); 
   
   //левый передний мотор 
   PORTC &= ~( 1 << PC3 ); 
   PORTC &= ~( 1 << PC2 );  

   //левый задний мотор 
   PORTC |=  ( 1 << PC4 ); 
   PORTC &= ~( 1 << PC5 );  

   //правый передний мотор 
   PORTD |=  ( 1 << PD7 ); 
   PORTB &= ~( 1 << PB0 );  

   //правый задний мотор 
   PORTD &= ~( 1 << PD6 ); 
   PORTB &= ~( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "moving diagonally to the left up"; 
   //UART_message(lng, mystr);  
} 
 
//Движение вправо вниз по диагонали 
void right_down_diagonal() 
{ 
   //светодиод 
   PORTB |=  ( 1 << PB6 ); 
   
   //левый передний мотор 
   PORTC &= ~( 1 << PC3 ); 
   PORTC &= ~( 1 << PC2 );  

   //левый задний мотор 
   PORTC &= ~( 1 << PC4 ); 
   PORTC |=  ( 1 << PC5 );  

   //правый передний мотор 
   PORTD &= ~( 1 << PD7 ); 
   PORTB |=  ( 1 << PB0 );  

   //правый задний мотор 
   PORTD &= ~( 1 << PD6 ); 
   PORTB &= ~( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "moving diagonally to the right down"; 
   //UART_message(lng, mystr);  
 
} 
 
//Движение влево вниз по диагонали 
void left_down_diagonal() 
{ 
   //светодиод 
   PORTB |=  ( 1 << PB6 ); 
   
   //левый передний мотор 
   PORTC &= ~( 1 << PC3 ); 
   PORTC |=  ( 1 << PC2 );  

   //левый задний мотор 
   PORTC &= ~( 1 << PC4 ); 
   PORTC &= ~( 1 << PC5 );  

   //правый передний мотор 
   PORTD &= ~( 1 << PD7 ); 
   PORTB &= ~( 1 << PB0 );  

   //правый задний мотор 
   PORTD &= ~( 1 << PD6 ); 
   PORTB |=  ( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "moving diagonally to the left down"; 
   //UART_message(lng, mystr);  
} 
 
//Поворот вокруг своей оси вправо 
void right_rotate() 
{ 
 //светодиод 
   PORTB |=  ( 1 << PB6 ); 
   
   //левый передний мотор 
   PORTC |=  ( 1 << PC3 ); 
   PORTC &= ~( 1 << PC2 );  

   //левый задний мотор 
   PORTC |=  ( 1 << PC4 ); 
   PORTC &= ~( 1 << PC5 );  

   //правый передний мотор 
   PORTD &= ~( 1 << PD7 ); 
   PORTB |=  ( 1 << PB0 );  

   //правый задний мотор 
   PORTD &= ~( 1 << PD6 ); 
   PORTB |=  ( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "rotation around the axis to the right"; 
   //UART_message(lng, mystr);  
} 
 
//Поворот вокруг своей оси влево 
void left_rotate() 
{ 
 //светодиод 
   PORTB |=  ( 1 << PB6 ); 
 
   //левый передний мотор 
   PORTC &= ~( 1 << PC3 ); 
   PORTC |=  ( 1 << PC2 );  

   //левый задний мотор 
   PORTC &= ~( 1 << PC4 ); 
   PORTC |=  ( 1 << PC5 );  

   //правый передний мотор 
   PORTD |=  ( 1 << PD7 ); 
   PORTB &= ~( 1 << PB0 );  

   //правый задний мотор 
   PORTD |=  ( 1 << PD6 ); 
   PORTB &= ~( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "rotation around the axis to the left"; 
   //UART_message(lng, mystr);  
} 
 
//Поворот вокруг некоторой оси вправо 
void right_arc_rotate() 
{ 
 //светодиод 
   PORTB |=  ( 1 << PB6 ); 
   
   //левый передний мотор 
   PORTC |=  ( 1 << PC3 ); 
   PORTC &= ~( 1 << PC2 );  

   //левый задний мотор 
   PORTC &= ~( 1 << PC4 ); 
   PORTC &= ~( 1 << PC5 );  

   //правый передний мотор 
   PORTD &= ~( 1 << PD7 ); 
   PORTB |=  ( 1 << PB0 );  

   //правый задний мотор 
   PORTD &= ~( 1 << PD6 ); 
   PORTB &= ~( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "rotation around the axis to the left"; 
   //UART_message(lng, mystr);  
} 
 
//Поворот вокруг некоторой оси влево 
void left_arc_rotate() 
{ 
 //светодиод 
   PORTB |=  ( 1 << PB6 ); 
   
   //левый передний мотор 
   PORTC &= ~( 1 << PC3 ); 
   PORTC |=  ( 1 << PC2 );  

   //левый задний мотор 
   PORTC &= ~( 1 << PC4 ); 


   PORTC &= ~( 1 << PC5 );  

   //правый передний мотор 
   PORTD |=  ( 1 << PD7 ); 
   PORTB &= ~( 1 << PB0 );  

   //правый задний мотор 
   PORTD &= ~( 1 << PD6 ); 
   PORTB &= ~( 1 << PB2 ); 

   //вывод сообщения 
   //mystr = "rotation around the axis to the left"; 
   //UART_message(lng, mystr);  
} 
 
 
void pin_init(void)  
{ 
   DDRB  |=  ( 1 << MOTOR_PB ); 
   PORTB &= ~( 1 << MOTOR_PB ); 

   DDRB  |=  ( 1 << MOTOR_PB_2 ); 
   PORTB &= ~( 1 << MOTOR_PB_2 ); 
} 
 
void timer1_init(void)  
{ 
   TCCR1A |= (1 << COM1A1) | (1 << WGM11); 
   TCCR1B |= (1 << WGM13)  | (1 << WGM12) | (1 << CS10); 
   TCNT1 = 0x00; 
   ICR1 = 0xFF; 
   OCR1A = 0x00; 
} 
 
void timer2_init(void)  
{ 
   TCCR2 |= (1 << WGM20) | (1 << WGM21) | (1 << COM21) | (1 << CS20); 
   //ASSR=0x08; 
   TCNT2 = 0x00; 
   OCR2 = 0x00; 
} 
/// 
 
void initUART() 
{ 
   UBRRL = 12; //4800 baud 
   UCSRB = (1<<TXEN) | (1<<RXEN) | (1<<RXCIE); 
   UCSRC = (1<<URSEL) | (3<<UCSZ0); 
} 
 
int writeSerial(char* str, char* str2, char* str3) 
{ 
   for(i = 0; str[i] != ':'; i++) 
   { 
      while(!(UCSRA & (1 << UDRE))){}; 
      UDR = str[i]; 
      if (i>0 && i<3){str2[i-1]=str[i];} 
      if (i>2){str3[i-3]=str[i];} 
   } 
   return 0; 
} 
 
int readSerial(char* str) 
{ 
   i = 0; 

   do { 
      while(!(UCSRA & (1 << RXC))) {}; 
      str[i] = UDR; 
      i++; 
   } while (str[i-1] != ':'); 

   unsigned char dummy; 
   while((UCSRA & (1 << RXC))) {dummy = UDR;}; 
   /** 
    while(!(UCSRA & (1 << RXC))) {}; 
   while((UCSRA & (1 << RXC))) { 
   str[i] = UDR; 
   i++; 
   }*/ 
   return 0; 
} 
 
ISR(USART_RXC_vect) 
{ 
   char bf = UDR; 
   data[IDX] = bf; 
   IDX++; 

   if (bf == ':') 
   { 
      IDX = 0; 
      done = 1; 
   } 
} 
 
inline void clearStr(char* str) 
{ 
   for(IT = 0; IT<LEN; IT++){str[IT]=0;} 
} 
 
int main() 
 
{ 
   // 
   DDRC  |=  ( 1 << 2 );  
   DDRC  |=  ( 1 << 3 );  
   DDRC  |=  ( 1 << 4 );  
   DDRC  |=  ( 1 << 5 ); 

   PORTC |=  ( 1 << PC2 );   
   PORTC |=  ( 1 << PC3 ); 


   PORTC |=  ( 1 << PC4 ); 
   PORTC |=  ( 1 << PC5 ); 

   DDRB  |=  ( 1 << 0 );  
   DDRB  |=  ( 1 << 2 ); 
   DDRB  |=  ( 1 << 6 ); 

   PORTB |=  ( 1 << PB0 ); 
   PORTB |=  ( 1 << PB2 ); 
   PORTB |=  ( 1 << PB6 ); 

   DDRD  |=  ( 1 << 6 );  
   DDRD  |=  ( 1 << 7 );  

   PORTD |=  ( 1 << PD6 );   
   PORTD |=  ( 1 << PD7 ); 

   PORTB &= ~( 1 << PB6 ); 

   //stop();  
   // 
   stop(); 
   initUART(); 
   pin_init(); 
   timer1_init(); 
   timer2_init(); 


   MOTOR_PWM = 80; 
   MOTOR_PWM_2 = 80; 
   MOTOR_PWM = 0; 
   MOTOR_PWM_2 = 0; 

   //mystr = "Atmega8 UART ready!"; 
   //UART_message(lng, mystr); 

   int PWM; 
   int PWM_2; 
   IDX = 0; 
   done = 0; 
   sei(); 

   while (1) 
   { 
      if(done) 
      { 
         if (data[0] == 'a')  
         { 
            stop();  
         } 

         else if (data[0] == 'b') 
         { 
            forward(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 

            PWM_axis[0] = data[3]; 
            PWM_axis[1] = data[4]; 
            PWM_2 = atoi(PWM_axis); 
            MOTOR_PWM_2 = PWM_2; 
         } 
            
         else if (data[0] == 'c') 
         { 
            backward(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 
            
            PWM_axis[0] = data[3]; 
            PWM_axis[1] = data[4]; 
            PWM_2 = atoi(PWM_axis); 
            MOTOR_PWM_2 = PWM_2; 
         } 
            
         else if (data[0] == 'd') 
         { 
            right(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 
            
            PWM_axis[0] = data[3]; 
            PWM_axis[1] = data[4]; 
            PWM_2 = atoi(PWM_axis); 
            MOTOR_PWM_2 = PWM_2; 
         } 
            
         else if (data[0] == 'e') 
         { 
            left(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 
            
            PWM_axis[0] = data[3]; 
            PWM_axis[1] = data[4]; 
            PWM_2 = atoi(PWM_axis); 
            MOTOR_PWM_2 = PWM_2; 
         } 
            
         else if (data[0] == 'f') 
         { 
            right_up_diagonal(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2];  

            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 
            MOTOR_PWM_2 = PWM; 
         } 
            
         else if (data[0] == 'g') 
         { 
            left_up_diagonal(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 
            MOTOR_PWM_2 = PWM; 
         } 
            
         else if (data[0] == 'h') 
         {     
            right_down_diagonal(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 
            MOTOR_PWM_2 = PWM; 
         } 
            
         else if (data[0] == 'i') 
         {     
            left_down_diagonal(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 
            MOTOR_PWM_2 = PWM; 
         } 
            
         else if (data[0] == 'j') 
         { 
            right_rotate(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 
            MOTOR_PWM_2 = PWM; 
         } 
            
         else if (data[0] == 'k') 
         { 
            left_rotate(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 

            MOTOR_PWM = PWM; 
            MOTOR_PWM_2 = PWM; 
         } 
            
         else if (data[0] == 'm') 
         { 
            right_arc_rotate(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 
            
            PWM_axis[0] = data[3]; 
            PWM_axis[1] = data[4]; 
            PWM_2 = atoi(PWM_axis); 
            MOTOR_PWM_2 = PWM_2; 
         } 
            
         else if (data[0] == 'l') 
         { 
            left_arc_rotate(); 
            
            char PWM_axis[2]; 
            PWM_axis[0] = data[1]; 
            PWM_axis[1] = data[2]; 
            PWM = atoi(PWM_axis); 
            MOTOR_PWM = PWM; 
            
            PWM_axis[0] = data[3]; 
            PWM_axis[1] = data[4]; 
            PWM_2 = atoi(PWM_axis); 
            MOTOR_PWM_2 = PWM_2; 
         } 
            
         done = 0; 
         clearStr(data); 
      } 
   } 
} 
