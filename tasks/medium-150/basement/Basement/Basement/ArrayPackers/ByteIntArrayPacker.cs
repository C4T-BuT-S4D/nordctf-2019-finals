using System;

namespace Basement
{
	public class ByteIntArrayPacker : IArrayPacker<byte, int>
	{
		public ByteIntArrayPacker() { }

		public int[] Pack(byte[] array)
		{
			var result = new int[(array.Length + 3) / sizeof(int)];
			Buffer.BlockCopy(array, 0, result, 0, array.Length);
			return result;
		}

		public byte[] Unpack(int[] array)
		{
			var result = new byte[array.Length * sizeof(int)];
			Buffer.BlockCopy(array, 0, result, 0, result.Length);
			return result;
		}
	}
}
