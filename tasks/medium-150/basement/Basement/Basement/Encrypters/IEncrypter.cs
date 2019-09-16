using System;

namespace Basement
{
	public interface IEncrypter<TKey>
	{
		byte[] Encrypt(TKey key, byte[] plaintext);
		byte[] Decrypt(TKey key, byte[] ciphertext);
	}
}
