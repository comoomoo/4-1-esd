/**
 *	Libraries.
 */

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>
#include "neural_network_handler.h"


/**
 *	Global variables.
 */

/* Array of layers. */
layer_t* l;

/* Size of l. */
int l_size;


/**
 *	Functions' definition.
 */

/* Initializes layers, neurons, weiights and biases. */
void init_neural_network(int layers_number, int* neurons_number)
{
	/* Set the specific l_size; */
	l_size = layers_number;

	/* Allocate memory for layers array. */
	l = (layer_t*)malloc(l_size * sizeof(layer_t));

	/* Initialize seed. */
	srand(time(NULL));

	/* Allocate memory for neurons and weights. */
	for(int i = 0; i < l_size; i++)
	{	
        int nSize=neurons_number[i];//opt
		/* Set the specific n_size. */
		l[i].n_size = nSize;

		/* Neurons. */
		l[i].n = (neuron_t*)malloc(nSize * sizeof(neuron_t));

		/* Allocate memory for each neuron in the ith layer. */
		for(int j = 0; i > 0 && j < nSize; j++)
		{
            int wSize=neurons_number[i-1];//opt
			/* Set the specific w_size. */
			l[i].n[j].w_size = wSize;
	
			/* Weights.  */
			l[i].n[j].w = (weight_t*)malloc(wSize * sizeof(weight_t));

			/* Initialize weights. */
			for(int k = 0; k < wSize; k++)
			{
				/* Initialize weight value. */
				l[i].n[j].w[k].value = ((double)rand() / (double)((unsigned)RAND_MAX + 1) * 2) - 1;
			}
		}
	}
}

/* ReLU activation function.  */
double relu(double input)
{
	/* Returns ReLU's output. */
	return (input > 0 ? input : 0);
}

/* Softmax activation function. */
void softmax()
{
	/* Maximum value in output's z array. */
	double max = -9999;

	/* Index of maximum value in output's z array. */
	int max_index = -1;
    int limit=l[l_size-1].n_size;
	/* Temporary array. */
	double tmp_z[limit];

	/* Sum of logits. */
	double logits_sum = 0;

	/* Find max in output's z array. */
	for(int i = 0; i < limit; i++)
	{
		if(max < l[l_size - 1].n[i].z)
		{
			max = l[l_size - 1].n[i].z;
			max_index = i;
		}
	}

	/* Max-normalize output's z array into tmp_a to prevent instability. */
	for(int i = 0; i < limit; i++)
	{
		tmp_z[i] = l[l_size - 1].n[i].z - max;
	}

	/* Compute sum of logits. */
	for(int i = 0; i < limit; i++)
	{
		logits_sum += exp(tmp_z[i]);
	}

	/* Compute each element of the distribution. */
	for(int i = 0; i < limit; i++)
	{
		l[l_size - 1].n[i].a = exp(tmp_z[i]) / logits_sum;
	}
}

/* Cross entropy loss function.  */
double cross_entropy(double label)
{
	/* Store l[l_size - 1].n[(int)label].a value. */
	double tmp = l[l_size - 1].n[(int)label].a;

	/* Return loss value and prevent instability. */
	return (tmp == 0 ? (-1) * (log(0.000001) / log(2)) : (-1) * (log(tmp) / log(2)));
}

/* Computes forward pass. */
void compute_forward(double* image)
{
	/* Copy image to input layer. */
    int nSize=l[0].n_size; //opt
	for(int i = 0; i < nSize; i++)
	{
		l[0].n[i].a = image[i];
	}

	/* Iterate over the remaining layers. */
	for(int i = 1; i < l_size; i++)
	{
        nSize=l[i].n_size;//opt
		/* Compute z values and a values. */
		for(int j = 0; j < nSize; j++)
		{
			/* Add the bias to z. */
			l[i].n[j].z = l[i].n[j].b.value;
            int wSize=l[i].n[i].w_size;//opt
			/* Compute z for each neuron. */
			for(int k = 0; k < wSize; k++)
			{
				l[i].n[j].z += l[i].n[j].w[k].value * l[i - 1].n[k].a;
			}

			/* Check if current layer is not output layer. */
			if(i != l_size - 1)
			{
				/* Compute a for each neuron. */
				l[i].n[j].a = relu(l[i].n[j].z);
			}
		}
	}

	/* Compute a for the output layer. */
	softmax();
}

/* Computes backward pass. */
void compute_backward(double label, float learning_rate)
{
    int nSize=l[l_size-1].n_size;
	/* Compute output layer's error. */
	for(int i = 0; i < nSize; i++)
	{
		/* delta^L = a^L - y. */
		l[l_size - 1].n[i].err = l[l_size - 1].n[i].a - (i == (int)label ? 1 : 0);
	}

	/* Compute hidden layers' error. */
	for(int i = l_size - 2; i > 0; i--)
	{
        nSize=l[i+1].n_size;//opt
		/* Iterate over neurons of the (i + 1)th layer. */
		for(int j = 0; j < nSize; j++)
		{
            int wSize=l[i+1].n[j].w_size;//opt
			/* Iterate over weights of the (i + 1)th layer. */
			for(int k = 0; k < wSize; k++)
			{
				/* Compute partial error. */
				l[i].n[k].err += l[i + 1].n[j].w[k].value * l[i + 1].n[j].err;
			}
		}
        nSize=l[i].n_size; //opt
		/* Iterate over neurons of the ith layer. */
		for(int j = 0; j < nSize; j++)
		{
			/* delta^l = (delta^(i + 1) * (w^(i + 1)^T) Hadamard ReLU'(z^l)) */
			l[i].n[j].err *= (l[i].n[j].z < 0 ? 0 : 1);
		}
	}

	/* Compute dC_db and update bias, compute dC_dw and update weights. Iterate over layers. */
	for(int i = 1; i < l_size; i++)
	{
        nSize=l[i].n_size;		//opt
        /* Iterate over neurons. */
		for(int j = 0; j < nSize; j++)
		{
			/* dC_db^l_j = delta^l_j. */
			l[i].n[j].b.dC_db = l[i].n[j].err;

			/* Update bias. */
			l[i].n[j].b.value -= learning_rate * l[i].n[j].b.dC_db;
            int wSize=l[i].n[j].w_size;
			/* Iterate over weights. */
			for(int k = 0; k < wSize; k++)
			{
				/* dC_dw^l_jk = a^(l - 1)_k * err^l_j. */
				l[i].n[j].w[k].dC_dw = l[i - 1].n[k].a * l[i].n[j].err;

				/* Update weight. */
				l[i].n[j].w[k].value -= learning_rate * l[i].n[j].w[k].dC_dw; 
			}
		}
	}
}

/* Reset function.  */
void reset_neural_network()
{
	/* Iterate over layers. */
	for(int i = 0; i < l_size; i++)
	{	
        int nSize=l[i].n_size;
		/* Iterate over neurons. */
		for(int j = 0; j < nSize; j++)
		{
			/* Reset dC_db. */
			l[i].n[j].b.dC_db = 0;
            int wSize=l[i].n[j].w_size;
			/* Iterate over weights. */
			for(int k = 0; k < wSize; k++)
			{
				/* Reset dC_dw. */
				l[i].n[j].w[k].dC_dw = 0;
			}

			/* Reset err. */
			l[i].n[j].err = 0;
		}
	}
}

/* Frees memory. */
void free_neural_network_memory()
{
	/* Free l, n, w. */
	for(int i = 0; i < l_size; i++)
	{
		/* Free w. */
		for(int j = l[i].n_size-1; j >= 0; j--)
		{
			/* Check if there exist an i + 1 layer. */
			if(i < l_size - 1)
			{
				/* Free w. */
				free(l[i].n[j].w);
			}
		}
		
		/* Free n. */
		free(l[i].n);
	}

	/* Free l. */
	free(l);
}
