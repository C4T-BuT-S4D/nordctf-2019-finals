using System;

namespace Basement
{
	public class XorEncrypter : IEncrypter<int>
	{
		protected const int EncodingTimes = 16;

		protected readonly IBytesCoder bytesCoder;
		protected readonly IArrayPacker<byte, int> arrayPacker;
		protected readonly IKeyExpander<int> keyExpander;

		public XorEncrypter(
			IBytesCoder bytesCoder, 
			IArrayPacker<byte, int> arrayPacker, 
			IKeyExpander<int> keyExpander)
		{
			this.bytesCoder = bytesCoder;
			this.arrayPacker = arrayPacker;
			this.keyExpander = keyExpander;
		}

		public byte[] Encrypt(int key, byte[] plaintext)
		{
			var encodedPlaintext = bytesCoder.Encode(plaintext, EncodingTimes);
			var packedPlaintext = arrayPacker.Pack(encodedPlaintext);
			var expandedKey = keyExpander.Expand(key, packedPlaintext.Length);
			var packedCiphertext = Xor(expandedKey, packedPlaintext);
			return arrayPacker.Unpack(packedCiphertext);
		}

		public byte[] Decrypt(int key, byte[] ciphertext)
		{
			var packedCiphertext = arrayPacker.Pack(ciphertext);
			var expandedKey = keyExpander.Expand(key, packedCiphertext.Length);
			var packedPlaintext = Xor(expandedKey, packedCiphertext);
			var encodedPlaintext = arrayPacker.Unpack(packedPlaintext);
			return bytesCoder.Decode(encodedPlaintext, EncodingTimes);
		}

		protected int[] Xor(int[] array1, int[] array2)
		{
			var result = new int[Math.Min(array1.Length, array2.Length)];

			for (var i = 0; i < result.Length; i++)
				result[i] = array1[i] ^ array2[i];

			return result;
		}
	}
}
