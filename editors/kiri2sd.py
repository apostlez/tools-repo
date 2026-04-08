"""
KIRIKIRI2 savedata encode/decode

kirikiri2 save data structure (BMP embedded):
[BMP image data][UTF-16LE save text]
BMP header offset 2 (4 bytes, little-endian) = size of BMP portion
"""

import re
import os
import struct
import sys
import zlib


def is_bmp(data):
	return data[:2] == b'BM'


def IsUnicode(s):
	for i in s:
		if i == 0:
			return True
	return False


def decode_bmp(filename):
	"""BMP embedded format: split into .bmp and .txt"""
	with open(filename, "rb") as f:
		raw = f.read()
	bmp_size = struct.unpack_from('<I', raw, 2)[0]
	bmp_data = raw[:bmp_size]
	save_data = raw[bmp_size:]
	if not save_data:
		print("no save data found after BMP image")
		exit()
	base = filename
	bmp_out = base + ".bmp"
	txt_out = base + ".txt"
	with open(bmp_out, "wb") as f:
		f.write(bmp_data)
	with open(txt_out, "wb") as f:
		f.write(save_data)
	print(f"BMP image  -> {bmp_out} ({bmp_size} bytes)")
	print(f"Save data  -> {txt_out} ({len(save_data)} bytes)")
	print("Success!")


def encode_bmp(txt_filename):
	"""BMP embedded format: combine .bmp + .txt -> .ksd
	Usage: kiri2sd.py -e <savefile.ksd.txt>
	Expects a matching <savefile.ksd.bmp> in the same directory.
	"""
	base = txt_filename
	if base.endswith(".txt"):
		base = base[:-4]
	bmp_filename = base + ".bmp"
	if not os.path.exists(bmp_filename):
		print(f"BMP file not found: {bmp_filename}")
		exit()
	with open(bmp_filename, "rb") as f:
		bmp_data = f.read()
	with open(txt_filename, "rb") as f:
		save_data = f.read()
	out_filename = base
	with open(out_filename, "wb") as f:
		f.write(bmp_data)
		f.write(save_data)
	print(f"Combined   -> {out_filename} ({len(bmp_data) + len(save_data)} bytes)")
	print("Success!")


def decode_plain(filename):
	"""Plain compressed format: decompress and write .txt"""
	try:
		f = open(filename, "rb")
	except:
		print("fail to file access")
		exit()
	header = f.read(5)
	f.seek(0x10, os.SEEK_CUR)
	data = f.read()
	f.close()
	try:
		data = zlib.decompress(data)
	except zlib.error:
		data = zlib.decompress(data, -15)

	bExcept = False
	try:
		f = open(filename + ".txt", "wb")
	except:
		print("fail to write file.")
		exit()
	try:
		_unicode = lambda x: x.encode("utf-16-le")
		f.write(_unicode("Header Signature : "))
		f.write(_unicode(header.hex() + "\n"))
		f.write(_unicode("CodePage : "))
		CodePage = IsUnicode(data) and "unicode" or "shift-jis"
		f.write(_unicode(CodePage + "\n"))
		if CodePage == "unicode":
			f.write(data)
		else:
			f.write(_unicode(data.decode('shift-jis')))
	except:
		bExcept = True
		print("fail to write file. ( maybe convert to codepage ) !")
	finally:
		f.close()
		if bExcept:
			os.remove(filename + ".txt")
		else:
			print("Success!")


def encode_plain(filename):
	"""Plain compressed format: read .txt and compress to .ksd"""
	try:
		f = open(filename, "rb")
	except:
		print("fail to file access")
		exit()
	Signature = f.readline()
	Signature += b"\x00"
	CodePage = f.readline()
	f.seek(1, os.SEEK_CUR)
	CodePage = CodePage[1:] + b"\x00"
	data = f.read()
	f.close()

	try:
		Signature = Signature.decode("utf-16-le")
		CodePage = CodePage.decode("utf-16-le")
		Signatrue = re.split(":", re.sub(" ", "", Signature[:-1]))
		CodePage = re.split(":", re.sub(" ", "", CodePage[:-1]))
		Signatrue = bytes.fromhex(Signatrue[1])
		CodePage = CodePage[1]
		ucps = len(data)
		if CodePage != 'unicode':
			data = data.decode("utf-16-le").encode(CodePage)
		data = zlib.compress(data, zlib.Z_DEFAULT_COMPRESSION, -15)
		cps = len(data)
		if not isinstance(ucps, int) or not isinstance(cps, int):
			raise
	except:
		print("convert fail")
		exit()

	try:
		f = open(filename + ".ksd", "wb")
	except:
		print("fail to write file.")
		exit()
	f.write(Signatrue)
	f.write(struct.pack("<II", cps, 0))
	f.write(struct.pack("<II", ucps, 0))
	f.write(data)
	f.close()
	print("Success!")


def main():
	if len(sys.argv) < 3:
		print("Using : kiri2sd.py [-e|-d] <filename>")
		print("  -d <file.ksd>      : decode (BMP embedded or plain compressed)")
		print("  -e <file.ksd.txt>  : encode (BMP embedded: requires matching .ksd.bmp)")
		exit()

	if sys.argv[1] in ("-d", "-D"):
		filename = sys.argv[2]
		with open(filename, "rb") as f:
			header2 = f.read(2)
		if is_bmp(header2):
			decode_bmp(filename)
		else:
			decode_plain(filename)

	elif sys.argv[1] in ("-e", "-E"):
		filename = sys.argv[2]
		# Determine format by checking for matching .bmp file
		base = filename[:-4] if filename.endswith(".txt") else filename
		if os.path.exists(base + ".bmp"):
			encode_bmp(filename)
		else:
			encode_plain(filename)

	else:
		print("Incorrect parameter XD!!")


if __name__ == "__main__":
	main()
