
import matplotlib.pyplot as plt

mask = generate_mask(Pattern.STRIPES, 256, dict(Lengths=[200, 100, 50, 25, 12, 6], Mirrored=True, Orientation=True))
plt.imshow(mask, cmap='gray', interpolation='nearest')
plt.axis('off')  # Désactive les axes pour une image propre
plt.savefig("test.png", bbox_inches='tight', pad_inches=0)
plt.close()
mask = generate_mask(Pattern.STRIPES, 256, dict(Lengths=[200, 100, 50, 25, 12, 6], Mirrored=False, Orientation=False))
plt.imshow(mask, cmap='gray', interpolation='nearest')
plt.axis('off')  # Désactive les axes pour une image propre
plt.savefig("test2.png", bbox_inches='tight', pad_inches=0)
plt.close()

print(mask)