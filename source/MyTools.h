#include <stdlib.h>


#ifdef _WIN32

    /* You should define ADD_EXPORTS *only* when building the DLL. */
    #ifdef API_EXPORTS
        #define API_FUNC __declspec(dllexport)
    #else
        #define API_FUNC __declspec(dllimport)
    #endif

  /* Define calling convention in one place, for convenience. */
  #define APICALL __cdecl

#else /* _WIN32 not defined. */

    /* Define with no value on non-Windows OSes. */
    #define API_FUNC
    #define APICALL

#endif

#ifdef __cplusplus
extern "C"
{
#endif

/*给一维数组加上二维索引*/
double** build_2D_index(double* storage, int rows, int cols);
/*给一维数组加上三维索引*/
double*** build_3D_index(double* storage, int layers, int rows, int cols);

#ifdef __cplusplus
} // __cplusplus defined.
#endif