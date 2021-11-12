# Util Functions

### `random_avatar.py`

1. `random_avatar`, Returns Random Avatar Image, `args: gender`
```python
from utils.random_avatar import random_avatar
# A Random Male(ish) Avatar Image
random_image = random_avatar('male')
# A Random Female(ish) Avatar Image
random_image = random_avatar('female')

```

### `base.py`

1. `get_client_ip(request)` Returns Clients IP using request parameter,
```python
from utils.base import get_client_ip

def view(request, *args, **kwargs):
    client_ip = get_client_ip(request)
```

### crypto.py
1. `encrypt(string)`, `decrypt(string)` Encrypts data
```python
from utils.crypto import encrypt, decrypt

encrypted_data = encrypt("TEXT TO BE ENCRYPTED")
decrypted_data = decrypt(str("TEXT_TO_BE_DECRYPTED"))
```

### model_utils.py

1. `username_validator`, Validates username
```python
from utils.model_utils import username_validator

username_validator('_Tycoon')
# Returns False
username_validator('12345')
# Returns False
username_validator('Tycoon')
# Returns True
```
2. `has_chars`, Checks if string has any character
```python
from utils.model_utils import has_chars
has_chars("AbCD123")
# Returns True
has_chars("_123_--12")
# Returns False
```
3. `file_location`, Returns File Location of a file that will be saved via a model, The model field that belongs to the respective model must have a `user` field, This function saves files in the respective user's folder with unique name and id
```python
from utils.model_utils import file_location
from django.db import models

class File(models.Model):
    # File will be saved with 
    user = models.ForeignKey(to="User", on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_location)
```
4. `is_email`, Will Check If email_address is email or not
```python
from utils.model_utils import is_email
is_email("email@email.com")
# Returns True
is_email("abcd")
# Returns False
```
5. `compress` Compress Images
```python
from utils.model_utils import compress
# Compresses Image
compressed_image = compress("IMAGE.JPG")
```
6. `create_random_text`, Creates Random Text
```python
from utils.model_utils import create_random_text
text = create_random_text(13) # AHJFJWYOXBNWG
# Random Text Generated
```
7. `create_random_length` Creates random Text Length number
```python
from utils.model_utils import create_random_length_number
length = create_random_length_number(10) # 105895681
# arg: 10, It will create a 10 digit random number
```
8. `generate_random_image`, Returns Random Avatar Image
```python
from utils.model_utils import generate_random_image
image, filename = generate_random_image()
```