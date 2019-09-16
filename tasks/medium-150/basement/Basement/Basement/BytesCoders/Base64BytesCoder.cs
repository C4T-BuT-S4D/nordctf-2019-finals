using System;
using System.Text;

namespace Basement
{
	public class Base64BytesCoder : IBytesCoder
	{
		protected readonly Encoding encoding;

		public Base64BytesCoder(Encoding encoding) 
		{
			this.encoding = encoding;
		}

		public byte[] Encode(byte[] bytes, int times = 1)
		{
			var result = bytes;

			for (var i = 0; i < times; i++) 
			{
				var base64 = Convert.ToBase64String(result);
				result = encoding.GetBytes(base64);
			}

			return result;
		}

		public byte[] Decode(byte[] bytes, int times = 1)
		{
			var result = bytes;

			for (var i = 0; i < times; i++) 
			{
				var base64 = encoding.GetString(result);
				result = Convert.FromBase64String(base64);
			}

			return result;
		}
	}
}
