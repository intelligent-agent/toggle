
#ifndef ESSHADER_H
#define ESUTIL_H


GLuint ESUTIL_API esLoadShader ( GLenum type, const char *shaderSrc );
GLuint ESUTIL_API esLoadProgram ( const char *vertShaderSrc, const char *fragShaderSrc );

#endif
