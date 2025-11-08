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

#define MAX_LENGTH	100

#define MATCH_SCORE	2
#define MISMATCH_SCORE	-1
#define GAP_PENALTY	2

#define STOP		0
#define UP		1
#define LEFT		2
#define DIAG		3


main()
{ 
	int	i, j;
	int	m, n;
	int	alignmentLength, score, tmp;
	char	X[MAX_LENGTH+1] = "ATTA";
	char	Y[MAX_LENGTH+1] = "ATTTTA";

	int	F[MAX_LENGTH+1][MAX_LENGTH+1];		/* score matrix */
	int	trace[MAX_LENGTH+1][MAX_LENGTH+1];	/* trace matrix */
	int C[MAX_LENGTH+1][MAX_LENGTH+1];		/* count matrix */
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

	F[0][0] = 0;
	C[0][0] = 0;
	for ( i=1 ; i<=m ; i++ ) {
		F[i][0] = F[i-1][0] - GAP_PENALTY;
		C[i][0] = 1;
	}
	for ( j=1 ; j<=n ; j++ ) {
		F[0][j] = F[0][j-1] - GAP_PENALTY;
		C[0][j] = 1;
	}


 	/*
	 * Fill matrices
	 */

	for ( i=1 ; i<=m ; i++ ) {

		for ( j=1 ; j<=n ; j++ ) {
	
			if ( X[i-1]==Y[j-1] ) {
				score = F[i-1][j-1] + MATCH_SCORE;
			} else {
				score = F[i-1][j-1] + MISMATCH_SCORE;
			}
			trace[i][j] = DIAG;

			tmp = F[i-1][j] - GAP_PENALTY;
			if ( tmp>score ) {
				score = tmp;
				trace[i][j] = UP;
			}

			tmp = F[i][j-1] - GAP_PENALTY;
			if( tmp>score ) {
				score = tmp;
				trace[i][j] = LEFT;
			}

			F[i][j] = score;
			C[i][j] = 1;

			// Check DIAG move
			if ( score == F[i-1][j-1] + ( (X[i-1] == Y[j-1] ) ? MATCH_SCORE : MISMATCH_SCORE) ) {
				C[i][j] += C[i-1][j-1];
			}
			
			// If characters match, we don't count gap paths
			if ( X[i-1] == Y[j-1] ) {
				continue;
			}

			// Check UP move
			if ( score == F[i-1][j] - GAP_PENALTY ) {
				C[i][j] += C[i-1][j];
			}

			// Check LEFT move
			if ( score == F[i][j-1] - GAP_PENALTY ) {
				C[i][j] += C[i][j-1];
			}
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
	
	printf("Number of optimal alignments: %d\n", C[m][n]);
	
	return(1);
}
