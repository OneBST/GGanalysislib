#include "MyTools.h"
/*给一维数组加上二维索引*/
double** build_2D_index(double* storage, int rows, int cols)
{
    int i;
    double **index_ptr, *temp_ptr;
    index_ptr = (double**)malloc(rows * sizeof(void*));
    temp_ptr = storage;
    for(i=0; i<rows; i++)
    {
        index_ptr[i] = temp_ptr;
        temp_ptr += cols;
    }
    return index_ptr;
}
/*给一维数组加上三维索引*/
double*** build_3D_index(double* storage, int layers, int rows, int cols)
{
    int i;
    double ***index_layer, **index_row, *temp_ptr;
    index_row = (double**)malloc(layers * rows * sizeof(void*));
    index_layer = (double***)malloc(layers * sizeof(void*));
    //创建指向每一平面的每行的指针
    double *temp_ptr_row;
    temp_ptr_row = storage;
    for(i=0; i<layers*rows; i++)
    {
        index_row[i] = temp_ptr_row;
        temp_ptr_row += cols;
    }
    //创建指向平面内第一行指针的指针
    double **temp_ptr_layer;
    temp_ptr_layer = index_row;
    for(i=0; i<layers; i++)
    {
        index_layer[i] = temp_ptr_layer;
        temp_ptr_layer += rows;
    }
    return index_layer;
}