/*
 * To compile this C program, placing the executable file in 'global', type:
 *
 *      gcc -o global global_alignment.c
 *
 * To run the program, type:
 *
 *      ./global
 */

#include <stdio.h>
#include <assert.h>

#define MAX_LENGTH	100

#define STOP		0
#define UP		1
#define LEFT		2
#define DIAG		3

// Calculate minimum value for insert, delete and substitute
int min(int a, int b, int c) {
	int m = a;
	if (b < m) m = b;
	if (c < m) m = c;
	return m;
}

main()
{ 
	int	i, j;
	int	m, n;
	int	alignmentLength, score, tmp;
	int cost;
	char	X[MAX_LENGTH+1] = "ATCGAT";
	char	Y[MAX_LENGTH+1] = "ATACGT";

	int	F[MAX_LENGTH+1][MAX_LENGTH+1];		/* score matrix */
	int	trace[MAX_LENGTH+1][MAX_LENGTH+1];	/* trace matrix */
	char	alignX[MAX_LENGTH*2];		/* aligned X sequence */
	char	alignY[MAX_LENGTH*2];		/* aligned Y sequence */


	/*
	 * Find lengths of (null-terminated) strings X and Y
	 */
	m = 0;
	n = 0;
	while ( X[m] != 0 ) {
		m++;
	}
	while ( Y[n] != 0 ) {
		n++;
	}


	/*
	 * Initialise matrices
	 */

	for ( i=0 ; i<=m ; i++ ) {
		F[i][0] = i;
	}
	for ( j=0 ; j<=n ; j++ ) {
		F[0][j] = j;
	}


 	/*
	 * Fill matrices
	 */

	for ( i=1 ; i<=m ; i++ ) {

		for ( j=1 ; j<=n ; j++ ) {
	
			if ( X[i-1] == Y[j-1] ) {
				cost = 0;
			}
			else {
				cost = 1;
			}

			int delete = F[i-1][j] + 1;				// Remove from X
			int insert = F[i][j-1] + 1;				// Insert on X
			int substitute = F[i-1][j-1] + cost;	// Replace character

			F[i][j] = min(delete, insert, substitute);
 		}
	}


	/*
	 * Print score matrix
	 */

	printf("Score matrix:\n      ");
	for ( j=0 ; j<n ; ++j ) {
		printf("%5c", Y[j]);
	}
	printf("\n");
	for ( i=0 ; i<=m ; i++ ) {
		if ( i==0 ) {
			printf(" ");
		} else {
			printf("%c", X[i-1]);
		}
		for ( j=0 ; j<=n ; j++ ) {
			printf("%5d", F[i][j]);
		}
		printf("\n");
	}
	printf("\n");

	/*
	 * Print alignment
	 */

	for ( i=alignmentLength-1 ; i>=0 ; i-- ) {
		printf("%c",alignX[i]);
	}

	printf("Levenshtein Distance = %d\n", F[m][n]);
	
	/* Testing */

	/* Distance should never be negative */
	assert(F[m][n] >= 0);

	return(1);
}
