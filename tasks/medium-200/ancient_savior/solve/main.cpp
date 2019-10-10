#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "main.h"
 
int main()
{
    FILE * pFile = fopen("enc.bmp", "rb");
 
    // считываем заголовок файла
    BITMAPFILEHEADER header __attribute__((unused));
 
    header.bfType      = read_u16(pFile);
    header.bfSize      = read_u32(pFile);
    header.bfReserved1 = read_u16(pFile);
    header.bfReserved2 = read_u16(pFile);
    header.bfOffBits   = read_u32(pFile);
 
    // считываем заголовок изображения
    BITMAPINFOHEADER bmiHeader;
 
    bmiHeader.biSize          = read_u32(pFile);
    bmiHeader.biWidth         = read_s32(pFile);
    bmiHeader.biHeight        = read_s32(pFile);
    bmiHeader.biPlanes        = read_u16(pFile);
    bmiHeader.biBitCount      = read_u16(pFile);
    bmiHeader.biCompression   = read_u32(pFile);
    bmiHeader.biSizeImage     = read_u32(pFile);
    bmiHeader.biXPelsPerMeter = read_s32(pFile);
    bmiHeader.biYPelsPerMeter = read_s32(pFile);
    bmiHeader.biClrUsed       = read_u32(pFile);
    bmiHeader.biClrImportant  = read_u32(pFile);
 
 
    RGBQUAD *rgb = new RGBQUAD[bmiHeader.biWidth * bmiHeader.biHeight];
 
    for (int i = 0; i < bmiHeader.biWidth * bmiHeader.biHeight; i++) {
        rgb[i].rgbBlue = getc(pFile);
        rgb[i].rgbGreen = getc(pFile);
        rgb[i].rgbRed = getc(pFile);
        getc(pFile);
    }
 
    // выводим результат
    for (int i = 0; i < 33 * 8; i++) {
        printf("%d", rgb[i].rgbBlue - 120);
    }
    printf("\n");
    fclose(pFile);
    return 0;
}
 
 
static unsigned short read_u16(FILE *fp)
{
    unsigned char b0, b1;
 
    b0 = getc(fp);
    b1 = getc(fp);
 
    return ((b1 << 8) | b0);
}
 
 
static unsigned int read_u32(FILE *fp)
{
    unsigned char b0, b1, b2, b3;
 
    b0 = getc(fp);
    b1 = getc(fp);
    b2 = getc(fp);
    b3 = getc(fp);
 
    return ((((((b3 << 8) | b2) << 8) | b1) << 8) | b0);
}
 
 
static int read_s32(FILE *fp)
{
    unsigned char b0, b1, b2, b3;
 
    b0 = getc(fp);
    b1 = getc(fp);
    b2 = getc(fp);
    b3 = getc(fp);
 
    return ((int)(((((b3 << 8) | b2) << 8) | b1) << 8) | b0);
}