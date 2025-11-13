#include "helpers.h"
#include <math.h>
#include <stdbool.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // find the avg of a pixel
            int avg =
                round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            // update the pixel to the avg
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // convert pixel to their sepia variant
            int sepr = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen +
                             .189 * image[i][j].rgbtBlue);
            if (sepr > 255)
            {
                sepr = 255;
            }
            int sepg = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen +
                             .168 * image[i][j].rgbtBlue);
            if (sepg > 255)
            {
                sepg = 255;
            }
            int sepb = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen +
                             .131 * image[i][j].rgbtBlue);
            if (sepb > 255)
            {
                sepb = 255;
            }
            // update the pixel to the sepia variant
            image[i][j].rgbtRed = sepr;
            image[i][j].rgbtGreen = sepg;
            image[i][j].rgbtBlue = sepb;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // buffer last pixel of row
            int bufferr = image[i][width - 1 - j].rgbtRed;
            int bufferg = image[i][width - 1 - j].rgbtGreen;
            int bufferb = image[i][width - 1 - j].rgbtBlue;

            // swap pixels of row
            image[i][width - 1 - j].rgbtRed = image[i][j].rgbtRed;
            image[i][width - 1 - j].rgbtGreen = image[i][j].rgbtGreen;
            image[i][width - 1 - j].rgbtBlue = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = bufferr;
            image[i][j].rgbtGreen = bufferg;
            image[i][j].rgbtBlue = bufferb;
        }
    }
    return;
}

// check if a pixel is out of bounds on a 3x3 grid of the initial pixel
// iterate over a valid 3x3 grid of the initial pixel
bool is_valid(int x, int y, int width, int height)
{
    return (0 <= x && x < width) && (0 <= y && y < height);
}
// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumr = 0, sumg = 0, sumb = 0;
            float count = 0;
            // get the pixel

            // NW
            if (is_valid(j - 1, i - 1, width, height))
            {
                sumr += image[i - 1][j - 1].rgbtRed;
                sumg += image[i - 1][j - 1].rgbtGreen;
                sumb += image[i - 1][j - 1].rgbtBlue;
                count++;
            }
            // N
            if (is_valid(j, i - 1, width, height))
            {
                sumr += image[i - 1][j].rgbtRed;
                sumg += image[i - 1][j].rgbtGreen;
                sumb += image[i - 1][j].rgbtBlue;
                count++;
            }
            // NE
            if (is_valid(j + 1, i - 1, width, height))
            {
                sumr += image[i - 1][j + 1].rgbtRed;
                sumg += image[i - 1][j + 1].rgbtGreen;
                sumb += image[i - 1][j + 1].rgbtBlue;
                count++;
            }
            // W
            if (is_valid(j - 1, i, width, height))
            {
                sumr += image[i][j - 1].rgbtRed;
                sumg += image[i][j - 1].rgbtGreen;
                sumb += image[i][j - 1].rgbtBlue;
                count++;
            }
            // C
            sumr += image[i][j].rgbtRed;
            sumg += image[i][j].rgbtGreen;
            sumb += image[i][j].rgbtBlue;
            count++;

            // E
            if (is_valid(j + 1, i, width, height))
            {
                sumr += image[i][j + 1].rgbtRed;
                sumg += image[i][j + 1].rgbtGreen;
                sumb += image[i][j + 1].rgbtBlue;
                count++;
            }
            // SW
            if (is_valid(j - 1, i + 1, width, height))
            {
                sumr += image[i + 1][j - 1].rgbtRed;
                sumg += image[i + 1][j - 1].rgbtGreen;
                sumb += image[i + 1][j - 1].rgbtBlue;
                count++;
            }
            // S
            if (is_valid(j, i + 1, width, height))
            {
                sumr += image[i + 1][j].rgbtRed;
                sumg += image[i + 1][j].rgbtGreen;
                sumb += image[i + 1][j].rgbtBlue;
                count++;
            }
            // SE
            if (is_valid(j + 1, i + 1, width, height))
            {
                sumr += image[i + 1][j + 1].rgbtRed;
                sumg += image[i + 1][j + 1].rgbtGreen;
                sumb += image[i + 1][j + 1].rgbtBlue;
                count++;
            }

            // make the average of all the colors on that 3x3 grid, round the values
            // make that pixel with the average on a copy
            copy[i][j].rgbtRed = round(sumr / count);
            copy[i][j].rgbtGreen = round(sumg / count);
            copy[i][j].rgbtBlue = round(sumb / count);

            // and cap at 255
            if (copy[i][j].rgbtRed > 255)
            {
                copy[i][j].rgbtRed = 255;
            }
            if (copy[i][j].rgbtGreen > 255)
            {
                copy[i][j].rgbtGreen = 255;
            }
            if (copy[i][j].rgbtBlue > 255)
            {
                copy[i][j].rgbtBlue = 255;
            }
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}
