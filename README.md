# EPISODE
This repository provides various codes used for the EPISODE project.

---

## Astrometry

**Astrometry_Method.ipynb** shows the procedure used for the astrometry correction of JWST IFU cube data. </br>
For the MIRI cubes, the centroid of the integrated intensity map is matched with the ALMA continuum centroid. </br>
For the NIRSpec cubes, scattered light shifts the centroid. The peak position of the integrated intensity map is matched with the ALMA continuum centroid.

---

## Silicate Fitting

The following files are included:
- **quartz-*-Zeidler2013-lnk** : optool input files for quartz (Zeidler et al. 2013, A&A)
- **make_opacity.py** : code for opacity generation of 6 silicates
- **silicate_*.txt** : generated opacities used for the MCMC fitting
- **Spec_Emission_tau_B_revision.txt** : Silicate emission optical depth spectrum of EC 53
- **Final_MCMC.ipynb** : code for opacity profile baseline fitting & MCMC fitting of the observed optical depth spectrum
