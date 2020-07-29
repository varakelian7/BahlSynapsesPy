#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _IKM_reg();
extern void _SlowCa_reg();
extern void _cad_reg();
extern void _h_reg();
extern void _kca_reg();
extern void _kfast_reg();
extern void _kslow_reg();
extern void _my_exp2syn_reg();
extern void _mynetstim_reg();
extern void _nap_reg();
extern void _nat_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," IKM.mod");
fprintf(stderr," SlowCa.mod");
fprintf(stderr," cad.mod");
fprintf(stderr," h.mod");
fprintf(stderr," kca.mod");
fprintf(stderr," kfast.mod");
fprintf(stderr," kslow.mod");
fprintf(stderr," my_exp2syn.mod");
fprintf(stderr," mynetstim.mod");
fprintf(stderr," nap.mod");
fprintf(stderr," nat.mod");
fprintf(stderr, "\n");
    }
_IKM_reg();
_SlowCa_reg();
_cad_reg();
_h_reg();
_kca_reg();
_kfast_reg();
_kslow_reg();
_my_exp2syn_reg();
_mynetstim_reg();
_nap_reg();
_nat_reg();
}
