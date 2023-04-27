### HMAC in C

This is a small and portable implementation of the [HMAC algorithm](https://en.wikipedia.org/wiki/HMAC) written in C.

Description from Wikipedia (emphasis added):

> In cryptography, an HMAC (sometimes expanded as either keyed-hash message authentication code or hash-based message authentication code) is a specific type of message authentication code (MAC) involving a cryptographic hash function and a secret cryptographic key. **As with any MAC, it may be used to simultaneously verify both the data integrity and the authenticity of a message.**
> 
> **HMAC can provide message authentication using a shared secret instead of using digital signatures with asymmetric cryptography**. It trades off the need for a complex public key infrastructure by delegating the key exchange to the communicating parties, who are responsible for establishing and using a trusted channel to agree on the key prior to communication.

---

The API looks like this (I am using C99 `<stdint.h>`-style annotated types):

```C
#define HMAC_SHA1_HASH_SIZE 20

/***********************************************************************'
