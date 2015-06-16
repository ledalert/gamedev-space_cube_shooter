#encoding=utf-8

from PIL import Image
import io, struct

def LoadVoxel(filename):
	with open(filename, 'rb') as f:
		width, height, depth, layers, images = struct.unpack('i'*5, f.read(4*5))
		image_list = [None] * images
		for image in range(images):
			png_length, = struct.unpack('i', f.read(4))
			png_data = io.BytesIO(f.read(png_length))
			image_list[image] = Image.open(png_data)

		for layer in range(layers):
			str_length, = struct.unpack('i', f.read(4))
			layer_name = f.read(str_length)

			visible, locked = struct.unpack('b' * 2, f.read(2))
			lw, lh, ld, lx, ly, lz = struct.unpack('i' * 6, f.read(4*6))
			
			voxel = dict()
			for x in range(lw):
				img_id, = struct.unpack('i', f.read(4))
				for y in range(lh):
					for z in range(ld):
						voxel[x,y,z] = image_list[img_id].getpixel((y,z))

			return visible, locked, lw, lh, ld, lx, ly, lz, voxel



if __name__ == '__main__':
	visible, locked, lw, lh, ld, lx, ly, lz, voxel = LoadVoxel('toaster.pnx')
	#r=''
	# for y in range(lh):
	# 	for x in range(lw):
	# 		r += '##' if voxel[x, y, 4][3] == 255 else '  '
	# 	r+='\n'


	cubes = list()
	for z in range(ld):
		for y in range(lh):
			for x in range(lw):
				if voxel[x,y,z][3] == 255:
					r,g,b=voxel[x,y,z][:3]
					cubes.append('{%i,%i,%i,%f,%f,%f}' % (x, y, z,r/255.0,g/255.0,b/255.0))

	print('#define CUBES (struct cube[]){%s}' % ','.join(cubes))
	print(len(cubes))