""" Tests pour la génération d'images """

import numpy as np

from SampleMaker.Mask import Mask
from SampleMaker.Pattern import Pattern
from SampleMaker.SampleGenerator import add_snr, apply_mask, compute_molecule_grid, compute_molecule_localisation, compute_molecule_number, compute_psf, generate_sample


###################################################
#def test_compute_molecule_number():
#	"""
#	Test de la fonction compute_molecule_numbert avec différentes valeurs en entrée.
#	"""
#
#	res = compute_molecule_number(100, 100, 1.0)
#	assert res == 100, f"le résultat est {res} au lieu de 100"
#
#	res = compute_molecule_number(256, 160, 0.1)
#	assert res == 167, f"le résultat est {res} au lieu de 167"
#
#	res = compute_molecule_number(256, 160, 0.25)
#	assert res == 419, f"le résultat est {res} au lieu de 419"
#
#	res = compute_molecule_number(256, 160, 0.5)
#	assert res == 838, f"le résultat est {res} au lieu de 838"
#
#	res = compute_molecule_number(256, 160, 1.0)
#	assert res == 1677, f"le résultat est {res} au lieu de 1677"
#
#
###################################################
#def test_compute_molecule_localisation():
#	"""
#	Test de la fonction compute_molecule_localisation.
#	"""
#
#	res = compute_molecule_localisation(size=100, pixel_size=100, density=1.0)
#	assert res.shape == (100, 3), f"Le résultat est {res.shape} au lieu de (100,3)"
#
#	res = compute_molecule_localisation(256, 160, 0.25)
#	assert res.shape == (419, 3), f"Le résultat est {res.shape} au lieu de (419,3)"
#
#
###################################################
#def test_compute_molecule_grid():
#	"""
#	Test de la fonction compute_molecule_localisation.
#	"""
#
#	res = compute_molecule_grid(size=100, shift=10)
#	assert res.shape == (81, 3), f"Le résultat est {res.shape} au lieu de (81,3)"
#
#
###################################################
#def test_apply_mask():
#	"""
#	Test de la fonction apply_mask.
#
#	.. todo:: Améliorer le test pour avoir un control total des entrées et sorties (un tableau localisation fixe et des masques simple), donc sans random.
#	"""
#
#	localisation = compute_molecule_localisation(256, 160, 0.25)
#	mask = generate_mask(MaskPattern.SQUARES, 256)
#	res = apply_mask(localisation, mask)
#	assert res.shape[0] <= 419, f"Le résultat possède plus de molécule ({res.shape[0]} au lieu de 419) après application du masque."
#
#	mask = generate_mask(MaskPattern.NONE, 256)
#	res = apply_mask(localisation, mask)
#	assert res.shape == (419, 3), f"Le résultat possède {res.shape[0]} molécules après application du masque blanc au lieu de 419."
#
#	res = apply_mask(localisation, ~mask)
#	assert res.shape == (0, 3), f"Le résultat possède {res.shape[0]} molécules après application du masque noir au lieu de 0."
#
#
###################################################
#def test_compute_psf():
#	"""
#	Test de la fonction compute_psf.
#
#	.. todo:: Améliorer le test pour avoir un control total des entrées (un tableau localisation fixe), donc sans random.
#	"""
#	localisation = compute_molecule_localisation(256, 160, 0.25)
#	res = compute_psf(256, localisation, 100.0, 10.0, 2.0)
#	assert res.shape == (256, 256), f"Le résultat est une image de taille {res.shape} au lieu de (256, 256)."
#
#
###################################################
#def test_compute_psf_bad_options():
#	"""
#	Test de la fonction compute_psf.
#	"""
#	localisation = compute_molecule_localisation(256, 160, 0.25)
#	res = compute_psf(256, localisation, 100.0, 10.0, 0)
#	assert res.shape == (256, 256), f"Le résultat est une image de taille {res.shape} au lieu de (256, 256)."
#	assert np.allclose(res, 0.0), f"Le résultat est une image contenant autre chose que du noir."
#
#
###################################################
#def test_add_snr():
#	"""
#	Test de la fonction add_snr.
#	"""
#	image = np.ones((256, 256), dtype=np.float32) * 500  # Exemple d'image avec des pixels égaux à 500
#	res = add_snr(image, snr=10, base_background=500, base_noise_std=12)
#	assert res.shape == (256, 256), f"Le résultat est une image de taille {res.shape} au lieu de (256, 256)."
#
#
###################################################
#def test_add_snr_bad():
#	"""
#	Test de la fonction add_snr avec une image nulle.
#	"""
#	image = np.zeros((256, 256), dtype=np.float32)  # Exemple d'image avec des pixels égaux à 500
#	res = add_snr(image, snr=10, base_background=500, base_noise_std=12)
#	assert res.shape == (256, 256), f"Le résultat est une image de taille {res.shape} au lieu de (256, 256)."
#
#
###################################################
#def test_generate_sample():
#	"""
#	Test de la fonction generate_sample.
#	"""
#
#	res = generate_sample(256, 160, 1.0, MaskPattern.NONE, None, 100, 10, 2, 10)
#	assert res.shape == (256, 256), f"Le résultat est une image de taille {res.shape} au lieu de (256, 256)."
