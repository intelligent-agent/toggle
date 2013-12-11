//
// Book:      OpenGL(R) ES 2.0 Programming Guide
// Authors:   Aaftab Munshi, Dan Ginsburg, Dave Shreiner
// ISBN-10:   0321502795
// ISBN-13:   9780321502797
// Publisher: Addison-Wesley Professional
// URLs:      http://safari.informit.com/9780321563835
//            http://www.opengles-book.com
//

// Simple_VertexShader.c
//
//    This is a simple example that draws a rotating cube in perspective
//    using a vertex shader to transform the object
//
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>
#include "esUtil.h"
#include "esShader.h"

#define DEBUG 1
#define debug_print(fmt, ...) \
        do { if (DEBUG) fprintf(stderr, "%s:%d:%s(): " fmt, __FILE__, \
                                __LINE__, __func__, __VA_ARGS__); } while (0)
typedef struct
{
    float x, y, z;
} vector;


typedef struct
{
   // Handle to a program object
   GLuint programObject;

   // Attribute locations
   GLint  positionLoc;
   GLint  normalLoc;
   GLint  colorLoc;

   // Uniform locations
   GLint  mvpLoc;
   GLint  mvLoc;
   GLint  lightLoc;
   
   // Vertex data
   GLfloat  *points;
   GLfloat  *vertex_normals;
   GLfloat  *colors;
   GLuint   *indices;
   int       numIndices;
   
   //Light data
   GLint    *lightPos;

   // Rotation angle
   GLfloat   angle;

   // MVP matrix
   ESMatrix  mvpMatrix;
   
   // MV Matrix
   ESMatrix  mvMatrix;
} UserData;




vector normalize_vector(vector v)
{
    vector n;
    float length;
    
    //Get length of vector
    length = sqrt((v.x*v.x) + (v.y*v.y) + (v.z*v.z));
    
    //Compute normal vector
    n.x = v.x / length;
    n.y = v.y / length;
    n.z = v.z / length;
    
    return n;
}


///
// Load 3D model
//
int loadBinarySTL (char * filename, GLfloat scale, GLfloat **points, GLfloat **vertex_normals, GLfloat **colors, GLuint **indices )
{
    int numFacets;
    int numVertices;
    int numIndices;
    int numPoints;
    long fileSize;
    char *mBuffer;
    unsigned int i;
	unsigned char* sz;
    GLfloat *triangle_normals;
    FILE *fp;

	debug_print("%s\n", "opening file");
    fp = fopen ( filename , "rb" );
    if( !fp ) {
        perror(filename);
        exit(1);
    }

	debug_print("%s\n", "fseeking");
    fseek( fp , 0L , SEEK_END);
    fileSize = ftell( fp );
    rewind( fp );

	debug_print("callocing %ld bytes \n", fileSize);

    /* allocate memory for entire content */
    mBuffer = (char*) calloc(fileSize+1, sizeof(char));
    if( mBuffer == NULL ) {
        fclose(fp);
        fprintf(stderr, "memory alloc fails");
        exit(1);
    }

	debug_print("*(mBuffer+100) = %d\n", *(mBuffer+100));	

	debug_print("%s\n", "Copying file to buffer");

    /* copy the file into the buffer */
    if( 1!=fread( mBuffer , fileSize, 1 , fp) ) {
      fclose(fp);
      free(mBuffer);
      fprintf(stderr, "entire read fails");
      exit(1);
    }

	debug_print("%s\n", "closing file");

    /* Close the file */
    fclose(fp);    

    // Check file size
	if (fileSize < 84) {
		fprintf(stderr, "STL: file is too small for the header");
		exit(-1);
	}

	// skip the first 80 bytes
	sz = (unsigned char*)mBuffer + 80;

	// Read the number of facets
	numFacets = *((unsigned int*)sz);
	sz += 4;

	if (fileSize < 84 + numFacets*12*sizeof(GLfloat)) {
		fprintf(stderr, "STL: file is too small to hold all facets");
	    exit(-1);	
	}
	if (!numFacets) {
		fprintf(stderr, "STL: file is empty. There are no facets defined");
	    exit(-1);
	}

    numVertices = numFacets*3;
    numPoints = numVertices*3;
    numIndices = numFacets*3;  // 

	debug_print("%s\n", "Creating array");    

    //Create arrays
    *points             = malloc ( sizeof(GLfloat) * 3 * numPoints );       // All the points/positions
    *vertex_normals     = malloc ( sizeof(GLfloat) * 3 * numVertices ); 	// The vertex normals (3 floats per vertex)
    *colors             = malloc ( sizeof(GLfloat) * 9 * numVertices ); 	// The colors (Red, green, blue for each vertex)
    *indices            = malloc ( sizeof(GLuint) * 3 * numIndices );       // Indices saying which vertices are together

    triangle_normals    = malloc ( sizeof(GLfloat) * 3 * numFacets );   	// The triangle normals (3 floats per facet/triangle)

	debug_print("Traversing %d facets. sz=%p\n", numFacets, sz);  
	debug_print("*points has addr %p \n", *points);  

	for (i = 0; i < numFacets;++i)	{
		debug_print("Facet %d: sz=%p\n", i, sz);  
	
	    //Indices
	    (*indices)[3*i+0] = 3*i+0;
	    (*indices)[3*i+1] = 3*i+1;
	    (*indices)[3*i+2] = 3*i+2;

	    //Color Vertex 1
	    (*colors)[9*i+0] = 255.0;
	    (*colors)[9*i+1] = 0.0;
	    (*colors)[9*i+2] = 0.0;

	    //Color Vertex 2
	    (*colors)[9*i+3] = 255.0;
	    (*colors)[9*i+4] = 0.0;
	    (*colors)[9*i+5] = 0.0;

	    //Color Vertex 3
	    (*colors)[9*i+6] = 255.0;
	    (*colors)[9*i+7] = 0.0;
	    (*colors)[9*i+8] = 0.0;
	    
        //Ignore normal vector
		//sz += sizeof(GLfloat)*3;		

	    debug_print("Making Triangles, sz is %p\n", sz);  	    
        
        //Get Normal vector for triangle
		triangle_normals[3*i+0] = *((GLfloat*)sz);
		sz += sizeof(GLfloat);
		triangle_normals[3*i+1] = *((GLfloat*)sz);
		sz += sizeof(GLfloat);
		triangle_normals[3*i+2] = *((GLfloat*)sz);
		sz += sizeof(GLfloat);
		

        //Get Vertex 1
		//debug_print("Setting point %d to %d\n", 9*i+0, *((GLfloat*)sz) * scale);  	 
		(*points)[9*i+0] = ((GLfloat)*sz) * scale;
		sz += sizeof(GLfloat);
		(*points)[9*i+1] = ((GLfloat)*sz) * scale;
		sz += sizeof(GLfloat);
		(*points)[9*i+2] = ((GLfloat)*sz) * scale;
		sz += sizeof(GLfloat);
		
        //Get Vertex 2
		(*points)[9*i+3] = ((GLfloat)*sz) * scale;
		sz += sizeof(GLfloat);
		(*points)[9*i+4] = ((GLfloat)*sz) * scale;
		sz += sizeof(GLfloat);
		(*points)[9*i+5] = ((GLfloat)*sz) * scale;
		sz += sizeof(GLfloat);
		
        //Get Vertex 3
		(*points)[9*i+6] = ((GLfloat)*sz) * scale;
		sz += sizeof(GLfloat);
		(*points)[9*i+7] = ((GLfloat)*sz) * scale;
		sz += sizeof(GLfloat);
		(*points)[9*i+8] = ((GLfloat)*sz) * scale;
		sz += sizeof(GLfloat);
		
		printf("Vertex 3: (%f, %f, %f)\n", (*points)[3*i+6], (*points)[3*i+7], (*points)[3*i+8]);

        //If no normal vector was provided, calculate it:
        if (triangle_normals[3*i+0] + triangle_normals[3*i+1] + triangle_normals[3*i+2] == 0.0) 
        {		
		    vector U;
		    vector V;
		    vector n;
		
		    //Set Vector U to (Vertex 2 minus Vertex 1)
            U.x = (*points)[9*i+3] - (*points)[9*i+0];
		    U.y = (*points)[9*i+4] - (*points)[9*i+1];
		    U.z = (*points)[9*i+5] - (*points)[9*i+2];
		
		    //Set Vector V to (Vertex 3 minus Vertex 1)
		    V.x = (*points)[9*i+6] - (*points)[9*i+0];
		    V.y = (*points)[9*i+7] - (*points)[9*i+1];
		    V.z = (*points)[9*i+8] - (*points)[9*i+2];

            //Set Normal.x to (multiply U.y by V.z) minus (multiply U.z by V.y)
		    n.x = (U.y * V.z) - (U.z * V.y);
            //Set Normal.y to (multiply U.z by V.x) minus (multiply U.x by V.z)
		    n.y = ( (U.z * V.x) - (U.x * V.z) );
            //Set Normal.z to (multiply U.x by V.y) minus (multiply U.y by V.x)
		    n.z = (U.x * V.y) - (U.y * V.x);
		    
		    //Normalize vector
		    n = normalize_vector(n);
		    triangle_normals[3*i+0] = -n.x;
		    triangle_normals[3*i+1] = -n.y;
		    triangle_normals[3*i+2] = -n.z;
		     
    		//printf("Normal: (%f, %f, %f)\n", triangle_normals[3*i+0], triangle_normals[3*i+1], triangle_normals[3*i+2]);        
        }

		
		//Ignore color info
		//uint16_t color = *((uint16_t*)sz);
		sz += 2;

    }
    
    debug_print("%s\n", "Creating array");  


    //Compute per-vertex normals
/*
    for (i=0; i<numVertices; i++)
    {
        //Create empty normal vector
        vector N = {0, 0, 0};
        
        //Get current vertex:
        vector cv = { (*points)[3*i + 0], (*points)[3*i + 1], (*points)[3*i + 2] };
        
        //Iterate through all the triangles to find which ones this vertex belongs too
        unsigned int u;
        for (u = 0; u < numFacets; u++)
        {
            vector v1 = {(*points)[9*u + 0], (*points)[9*u + 1], (*points)[9*u + 2]};
            vector v2 = {(*points)[9*u + 3], (*points)[9*u + 4], (*points)[9*u + 5]};
            vector v3 = {(*points)[9*u + 6], (*points)[9*u + 7], (*points)[9*u + 8]};
            
            //Check if current vertex is in this triangle
            if (  (cv.x == v1.x && cv.y == v1.y && cv.z == v1.z) || 
                  (cv.x == v2.x && cv.y == v2.y && cv.z == v2.z) ||
                  (cv.x == v3.x && cv.y == v3.y && cv.z == v3.z)  )
            {
                N.x += triangle_normals[3*u + 0];
                N.y += triangle_normals[3*u + 1];
                N.z += triangle_normals[3*u + 2];
            }
        }
        
        //Normalize the normal vector
        N = normalize_vector(N);
        
        //Save vertex normal
        (*vertex_normals)[3*i + 0] = N.x;
        (*vertex_normals)[3*i + 1] = N.y;
        (*vertex_normals)[3*i + 2] = N.z;
    }
    */
    
    for (i = 0; i<numFacets; i++)
    {
    
        //Save vertex normal
        (*vertex_normals)[9*i + 0] = triangle_normals[3*i + 0];
        (*vertex_normals)[9*i + 1] = triangle_normals[3*i + 1];
        (*vertex_normals)[9*i + 2] = triangle_normals[3*i + 2];
        
        //Save vertex normal
        (*vertex_normals)[9*i + 3] = triangle_normals[3*i + 0];
        (*vertex_normals)[9*i + 4] = triangle_normals[3*i + 1];
        (*vertex_normals)[9*i + 5] = triangle_normals[3*i + 2];
        
        //Save vertex normal
        (*vertex_normals)[9*i + 6] = triangle_normals[3*i + 0];
        (*vertex_normals)[9*i + 7] = triangle_normals[3*i + 1];
        (*vertex_normals)[9*i + 8] = triangle_normals[3*i + 2];
        
        //printf("Normal: (%f, %f, %f)\n", triangle_normals[3*i+0], triangle_normals[3*i+1], triangle_normals[3*i+2]);        
      /*  printf("\nNormals:\n(");
        printf("%f, ", (*vertex_normals)[9*i + 0]);
        printf("%f, ", (*vertex_normals)[9*i + 1]);
        printf("%f, ", (*vertex_normals)[9*i + 2]);
        printf("%f, ", (*vertex_normals)[9*i + 3]);
        printf("%f, ", (*vertex_normals)[9*i + 4]);
        printf("%f, ", (*vertex_normals)[9*i + 5]);
        printf("%f, ", (*vertex_normals)[9*i + 6]);
        printf("%f, ", (*vertex_normals)[9*i + 7]);
        printf("%f)", (*vertex_normals)[9*i + 8]);
        */
    }
    
    /*for (i = 8; i<numFacets; i++)
    {
    
        //Save vertex normal
        (*vertex_normals)[9*i + 0] = 0;
        (*vertex_normals)[9*i + 1] = 0;
        (*vertex_normals)[9*i + 2] = 0;
        
        //Save vertex normal
        (*vertex_normals)[9*i + 3] = 0;
        (*vertex_normals)[9*i + 4] = 0;
        (*vertex_normals)[9*i + 5] = 0;
        
        //Save vertex normal
        (*vertex_normals)[9*i + 6] = 0;
        (*vertex_normals)[9*i + 7] = 0;
        (*vertex_normals)[9*i + 8] = 0;
        
        printf("\nNew normals:\n(");
        printf("%f, ", (*vertex_normals)[9*i + 0]);
        printf("%f, ", (*vertex_normals)[9*i + 1]);
        printf("%f, ", (*vertex_normals)[9*i + 2]);
        printf("%f, ", (*vertex_normals)[9*i + 3]);
        printf("%f, ", (*vertex_normals)[9*i + 4]);
        printf("%f, ", (*vertex_normals)[9*i + 5]);
        printf("%f, ", (*vertex_normals)[9*i + 6]);
        printf("%f, ", (*vertex_normals)[9*i + 7]);
        printf("%f)", (*vertex_normals)[9*i + 8]);
        
        
    }*/
        
    
	//Free buffers that are no longer used
    free(mBuffer);
    free(triangle_normals);
    
    printf("Facets: %d\n", numFacets);
    return numIndices;
}




///
// Initialize the shader and program object
//
int Init ( ESContext *esContext )
{
    esContext->userData = malloc(sizeof(UserData));
	
    UserData *userData = esContext->userData;
/*   GLbyte vShaderStr[] =  
      "uniform mat4 u_mvpMatrix;                   \n"
      "attribute vec4 a_position;                  \n"
      "void main()                                 \n"
      "{                                           \n"
      "   gl_Position = u_mvpMatrix * a_position;  \n"
      "}                                           \n";
*/

    GLbyte vShaderStr[] =
        "uniform mat4 u_MVPMatrix;      \n"     // A constant representing the combined model/view/projection matrix.
        "uniform mat4 u_MVMatrix;       \n"     // A constant representing the combined model/view matrix.
        //"uniform vec3 u_LightPos;       \n"     // The position of the light in eye space.
     
        "attribute vec4 a_Position;     \n"     // Per-vertex position information we will pass in.
        "attribute vec4 a_Color;        \n"     // Per-vertex color information we will pass in.
        "attribute vec3 a_Normal;       \n"     // Per-vertex normal information we will pass in.
     
        "varying vec4 v_Color;          \n"     // This will be passed into the fragment shader.
     
        "void main()                    \n"     // The entry point for our vertex shader.
        "{                              \n"
        "   vec3 u_LightPos = vec3(-50, -50, -50);                                     \n"
        
        //"   vec3 modelViewVertex = vec3(u_MVMatrix * a_Position);              \n" // Transform the vertex into eye space.
        //"   vec3 modelViewNormal = vec3(u_MVMatrix * vec4(a_Normal, 0.0));     \n" // Transform the normal's orientation into eye space.
        
        //"   float distance = length(u_LightPos - modelViewVertex);             \n" // Will be used for attenuation.
        "   float distance = length(vec4(u_LightPos, 0.0) - a_Position);             \n"
        
        //"   vec3 lightVector = normalize(u_LightPos - modelViewVertex);        \n" // Get a lighting direction vector from the light to the vertex.
        
        "   float diffuse = max(dot(a_Normal, u_LightPos)*1.0, 0.1);            \n"
        
        //"   float diffuse = max(dot(modelViewNormal, lightVector)*1.0, 0.1);       \n" // Calculate the dot product of the light vector and vertex normal. If the normal and light vector are pointing in the same direction then it will get max illumination.
        "   diffuse = diffuse * (1.0 / (1.0 + (0.25 * distance * distance)));  \n" // Attenuate the light based on distance.
        "   float ambient_light = 0.0010;                                         \n" // Ambient light
        "   v_Color = a_Color * diffuse;                                       \n" // Multiply the color by the illumination level. It will be interpolated across the triangle.        
        //"   v_Color = a_Color * (ambient_light + diffuse);                                       \n"
        //"   v_Color = a_Color * min((diffuse+ambient_light), 1.0);             \n" // Multiply the color by the illumination level. It will be interpolated across the triangle.
        //"   v_Color = a_Color;                                                \n"
        "   gl_Position = u_MVPMatrix * a_Position;                            \n" // gl_Position is a special variable used to store the final position. Multiply the vertex by the matrix to get the final point in normalized screen coordinates.
        "}                                                                     \n";

   
/*    GLbyte fShaderStr[] =  
        "precision mediump float;                            \n"
        "void main()                                         \n"
        "{                                                   \n"
        "  gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );        \n"
        "}                                                   \n";

*/
    GLbyte fShaderStr[] =  
        "precision mediump float;       \n"     // Set the default precision to medium. We don't need as high of a
                                                // precision in the fragment shader.
        "varying vec4 v_Color;          \n"     // This is the color from the vertex shader interpolated across the
                                                // triangle per fragment.
        "void main()                    \n"     // The entry point for our fragment shader.
        "{                              \n"
        "   gl_FragColor = v_Color;     \n"     // Pass the color directly through the pipeline.
        "}";    


    // Load the shaders and get a linked program object
    userData->programObject = esLoadProgram ( vShaderStr, fShaderStr );

    // Get the attribute locations
    userData->positionLoc = glGetAttribLocation ( userData->programObject, "a_Position" );
    userData->normalLoc = glGetAttribLocation ( userData->programObject, "a_Normal" );
    userData->colorLoc = glGetAttribLocation ( userData->programObject, "a_Color" );

    // Get the uniform locations
    userData->mvpLoc = glGetUniformLocation( userData->programObject, "u_MVPMatrix" );
    userData->mvLoc = glGetUniformLocation( userData->programObject, "u_MVMatrix" );
    //userData->lightLoc = glGetUniformLocation( userData->programObject, "u_LightPos" );

    //Create diffuse light position
    //userData->lightPos = (GLuint*) malloc( sizeof(GLuint) * 3 );
    //userData->lightPos[0] = 0;
    //userData->lightPos[1] = 0;
    //userData->lightPos[2] = 200;

    // Generate the vertex data
    //userData->numIndices = esGenCube( 1.0, &userData->points, NULL, NULL, &userData->indices );
    userData->numIndices = loadBinarySTL("0.4mm-thin-wall.stl", 0.5, &userData->points, &userData->vertex_normals, &userData->colors, &userData->indices);

    // Starting rotation angle for the cube
    userData->angle = 45.0f;

    glClearColor ( 0.0f, 0.0f, 0.0f, 1.0f );
    
    //glEnable(GL_CULL_FACE);
    //glCullFace(GL_BACK);

	debug_print("Init OK %d\n", 1);  	    
    
    return GL_TRUE;
}


///
// Update MVP matrix based on time
//
void Update ( ESContext *esContext, float deltaTime )
{
   UserData *userData = (UserData*) esContext->userData;
   ESMatrix perspective;
   ESMatrix modelview;
   float    aspect;
   
   // Compute a rotation angle based on time to rotate the cube
   userData->angle += ( deltaTime * 40.0f );
   if( userData->angle >= 360.0f )
      userData->angle -= 360.0f;

   // Compute the window aspect ratio
   aspect = (GLfloat) esContext->width / (GLfloat) esContext->height;
   
   // Generate a perspective matrix with a 45 degree FOV
   esMatrixLoadIdentity( &perspective );
   esPerspective( &perspective, 45.0f, aspect, 0.1f, 1500.0f );

   // Generate a model view matrix to rotate/translate the cube
   esMatrixLoadIdentity( &modelview );

   // Translate away from the viewer
   esTranslate( &modelview, 0.0, 0.0, -50.0 );

   // Rotate the cube
   esRotate( &modelview, userData->angle, 1.0, 0.0, 1.0 );
   
   // Compute the final MVP by multiplying the 
   // modevleiw and perspective matrices together
   esMatrixMultiply( &userData->mvpMatrix, &modelview, &perspective );
   
   //Copy the ModelView Matrix into userData
   userData->mvMatrix = modelview;
}

///
// Draw our scene
//
void Draw ( ESContext *esContext )
{
    UserData *userData = esContext->userData;

    // Set the viewport
    glViewport ( 0, 0, esContext->width, esContext->height );


    // Clear the color buffer
    glClear ( GL_COLOR_BUFFER_BIT );

    // Use the program object
    glUseProgram ( userData->programObject );

    // Load the vertex position, color and normal
    glVertexAttribPointer ( userData->positionLoc, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), userData->points );
    glVertexAttribPointer ( userData->normalLoc, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), userData->vertex_normals );
    glVertexAttribPointer ( userData->colorLoc, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), userData->colors );                           
                              
    glEnableVertexAttribArray ( userData->positionLoc );
    glEnableVertexAttribArray ( userData->normalLoc );
    glEnableVertexAttribArray ( userData->colorLoc );


    // Load the MVP matrix
    glUniformMatrix4fv( userData->mvpLoc, 1, GL_FALSE, (GLfloat*) &userData->mvpMatrix.m[0][0] );
    
    // Load the MVP matrix
    glUniformMatrix4fv( userData->mvLoc, 1, GL_FALSE, (GLfloat*) &userData->mvMatrix.m[0][0] );
    
    //Load the Light position
    //glUniform3iv(userData->lightLoc, 1, userData->lightPos);

    // Draw the cube
    glDrawElements ( GL_TRIANGLES, userData->numIndices, GL_UNSIGNED_INT, userData->indices );
}

///
// Cleanup
//
void ShutDown ( ESContext *esContext )
{
   UserData *userData = esContext->userData;

   if ( userData->points != NULL )
   {
      free ( userData->points );
   }

   if ( userData->indices != NULL )
   {
      free ( userData->indices );
   }

   if ( userData->vertex_normals != NULL )
   {
      free ( userData->vertex_normals );
   }
   
   if ( userData->colors != NULL )
   {
      free ( userData->colors );
   }
   
   free ( userData->lightPos );
   
   // Delete program object
   glDeleteProgram ( userData->programObject );

   free(userData);
}


int main ( int argc, char *argv[] ){

    ESContext esContext;
    UserData  userData;

    esInitContext ( &esContext );
    esContext.userData = &userData;

    esCreateWindow ( &esContext, "STL Viewer", 500, 500, ES_WINDOW_RGB );

    if ( !Init ( &esContext ) )
        return 0;

    esRegisterDrawFunc ( &esContext, Draw );
    esRegisterUpdateFunc ( &esContext, Update );

	debug_print("Entering main loop %d\n", 1);
    esMainLoop ( &esContext );

    ShutDown ( &esContext );

	return 0;
}




