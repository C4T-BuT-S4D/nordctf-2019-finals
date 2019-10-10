#include <iostream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "main.h"

std::string to_binary(std::string str) {
    std::string bits, var;
    for (int i = 0; i < str.size(); i++) {
        int copy = str[i];
        var = "";
        while (copy != 0) {
            var.push_back((copy % 2) + '0');
            copy = copy / 2;
        }
        while (var.size() != 8)
            var.push_back('0');
        for (int j = (var.size() - 1); j >= 0; j--)
            bits.push_back(var[j]);
    }
    return bits;
}

int main()
{
    std::string plain_file, enc_file;
    std::cout << "Hi! I can hide any text you want in bmp image!\nInput name of your picture: ";
    getline(std::cin, plain_file);
    std::cout << "Now input name of output file: ";
    getline(std::cin, enc_file);

    std::string text;
    std::cout << "Give me your secret text (ends with \\n): ";
    getline(std::cin, text);
    std::cout << "Starting hiding...\n";
    std::string bitmap = to_binary(text);

    FILE *pFile = fopen(plain_file.c_str(), "rb");
    if (pFile == 0){
        std::cout << "No such image.\n";
        exit(1);
    }

    BITMAPFILEHEADER header;
 
    header.bfType      = read_u16(pFile);
    header.bfSize      = read_u32(pFile);
    header.bfReserved1 = read_u16(pFile);
    header.bfReserved2 = read_u16(pFile);
    header.bfOffBits   = read_u32(pFile);

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
 
    if (bitmap.size() > (bmiHeader.biHeight * bmiHeader.biWidth)) {
        std::cout << "Too big text.\n";
        exit(1);
    }

    RGBQUAD *pixels = new RGBQUAD[bmiHeader.biHeight * bmiHeader.biWidth];
    
    for (int i = 0; i < bmiHeader.biHeight * bmiHeader.biWidth; i++) {
        pixels[i].rgbBlue = getc(pFile);
        pixels[i].rgbGreen = getc(pFile);
        pixels[i].rgbRed = getc(pFile);
        pixels[i].rgbReserved = getc(pFile);
    }
    fclose(pFile);
 
    
    FILE *oFile = fopen(enc_file.c_str(), "wb");
    if (oFile == 0) {
        std::cout << "Cant create result file.\n";
        exit(1);
    }
    write_u16(header.bfType, oFile);
    write_u32(header.bfSize, oFile);
    write_u16(header.bfReserved1, oFile);
    write_u16(header.bfReserved2, oFile);
    write_u32(header.bfOffBits, oFile);

    write_u32(bmiHeader.biSize, oFile);
    write_s32(bmiHeader.biWidth, oFile);
    write_s32(bmiHeader.biHeight, oFile);
    write_u16(bmiHeader.biPlanes, oFile);
    write_u16(bmiHeader.biBitCount, oFile);
    write_u32(bmiHeader.biCompression, oFile);
    write_u32(bmiHeader.biSizeImage, oFile);
    write_s32(bmiHeader.biXPelsPerMeter, oFile);
    write_s32(bmiHeader.biYPelsPerMeter, oFile);
    write_u32(bmiHeader.biClrUsed, oFile);
    write_u32(bmiHeader.biClrImportant, oFile);

    for (int i = 0; i < bmiHeader.biHeight * bmiHeader.biWidth; i++) {
        if (i < bitmap.size())
            putc(bitmap[i] - '0' + 120, oFile);
        else
            putc(pixels[i].rgbBlue, oFile);
        putc(pixels[i].rgbGreen, oFile);
        putc(pixels[i].rgbRed, oFile);
        putc(pixels[i].rgbReserved, oFile);
    }
 
    fclose(oFile);
    std::cout << "Completed :)\n";
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
 
static void write_u16(unsigned short input, FILE *fp)
{
    putc(input, fp);
    putc(input >> 8, fp);
}
 
static void write_u32(unsigned int input, FILE *fp)
{
    putc(input, fp);
    putc(input >> 8, fp);
    putc(input >> 16, fp);
    putc(input >> 24, fp);
}
 
static void write_s32(int input, FILE *fp)
{
    putc(input, fp);
    putc(input >> 8, fp);
    putc(input >> 16, fp);
    putc(input >> 24, fp);
}
