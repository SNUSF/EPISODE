#!/home/sjlee/miniforge3/envs/JWST/bin/python


# input example: ./make_opacity.py -dhs 0.99 -a 0.1 2.0 -comp c 0.13  -> geometry: DHS 0.99, size: 0.1 to 2.0 micron, composition: 13% carbon, rest silicate

import numpy as np
import optool
import sys
import re

optool_exec='~/Programs/optool/optool'
optool_lnk_path = '/home/sjlee/Programs/optool/lnk_data/ad/'


geometry_option='-dhs 0.99'
size_option='-a 0.1'
wave_option='-l 1.000 50.000 24501'
composition_option='1'
filename = 'silicate_kabs_'

if len(sys.argv) < 2:
    pass
else:
    input_str = ' '.join(sys.argv[1:])
    list_options = re.findall(r'-[a-zA-Z]+\s+[^-]+', input_str)
    
    for option in list_options:
        if len(option)<1:
            continue
        if option[-1]==' ':
            option = option[:-1]

        if option.split(' ')[0]=='-dhs' or option.split(' ')[0]=='-mmf' or option.split(' ')[0]=='-cde':
            geometry_option = option
        elif option.split(' ')[0]=='-a':
            size_option = option
        elif option.split(' ')[0]=='-l':
            wave_option = option
        elif option.split(' ')[0]=='-comp':
            numbers = re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', option)
            total = sum(map(float, numbers))
            composition_option = ' '.join([str(1-total)] + option.split(' ')[1:])

print(geometry_option)
print(size_option)
print(wave_option)
print(composition_option)

composition_option_filename = composition_option
composition_option_filename = ' '.join(composition_option_filename.split(' ')[1:])
if len(composition_option_filename)>0:
    filename=filename+geometry_option+'_'+size_option+'_'+composition_option_filename+'.txt'
else:
    filename=filename+geometry_option+'_'+size_option+'.txt'


p_oliv_1 = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, 'ol-mg50', composition_option]))

px = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, optool_lnk_path + 'pyr-c-mg96-x-Jaeger1998.lnk', composition_option]))
py = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, optool_lnk_path + 'pyr-c-mg96-y-Jaeger1998.lnk', composition_option]))
pz = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, optool_lnk_path + 'pyr-c-mg96-z-Jaeger1998.lnk', composition_option]))
p_enst_1 = (px+py+pz)/3.

p_pyrx_1 = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, 'pyr-mg70', composition_option]))

px = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, optool_lnk_path + 'ol-c-mg95-x-Fabian2001.lnk', composition_option]))
py = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, optool_lnk_path + 'ol-c-mg95-y-Fabian2001.lnk', composition_option]))
pz = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, optool_lnk_path + 'ol-c-mg95-z-Fabian2001.lnk', composition_option]))
p_fors_1 = (px+py+pz)/3.

p_silica_1 = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, 'sio2', composition_option]))

px = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, optool_lnk_path + 'quartz-x-Zeidler2013.lnk', composition_option]))
py = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, optool_lnk_path + 'quartz-y-Zeidler2013.lnk', composition_option]))
pz = optool.particle(' '.join([optool_exec, geometry_option, size_option, wave_option, optool_lnk_path + 'quartz-z-Zeidler2013.lnk', composition_option]))
p_quartz_1 = (px+py+pz)/3.




k_arr = np.zeros((len(p_pyrx_1.lam), 7))
k_arr[:, 0] = p_pyrx_1.lam
k_arr[:, 1] = p_oliv_1.kabs[0]
k_arr[:, 2] = p_fors_1.kabs[0]
k_arr[:, 3] = p_pyrx_1.kabs[0]
k_arr[:, 4] = p_enst_1.kabs[0]
k_arr[:, 5] = p_silica_1.kabs[0]
k_arr[:, 6] = p_quartz_1.kabs[0]

print('------------------------------')
print('Saving file to:', filename)

with open(filename, 'w') as f:
    f.write(geometry_option+'\n')
    f.write(size_option+'\n')
    #f.write(wave_option+'\n')
    f.write(composition_option+'\n')
    f.write("       lam   pyroxene    olivine  enstatite forsterite     silica     quartz\n")

    np.savetxt(f, k_arr, fmt="%10.5f")

f.close()
