# Texterify Client Library

This is an asynchronous client library for interacting with the Texterify localization platform. The library provides methods to manage projects, keys, and translations using the Texterify API.

## Installation

```bash
pip install texteripy
```

## Usage

### Initialization

```python
from texteripy import Texterify

texterify = Texterify(auth_email="your_email", auth_secret="your_secret")
```

### Retrieve Projects

```python
projects = await texterify.get_projects()
```

### Retrieve Keys for a Project

```python
project_id = "your_project_id"
keys = await texterify.get_keys(project_id)
```

### Create a Key

```python
project_id = "your_project_id"
key_name = "new_key_name"
key_description = "new_key_description"

new_key = await texterify.create_key(project_id, key_name, key_description)
```

### Update a Key

```python
project_id = "your_project_id"
key_id = "your_key_id"
new_key_name = "updated_key_name"
new_key_description = "updated_key_description"

updated_key = await texterify.update_key(project_id, key_id, new_key_name, new_key_description)
```

### Delete Keys

```python
project_id = "your_project_id"
keys_to_delete = ["key_id_1", "key_id_2"]

deleted_keys = await texterify.delete_keys(project_id, keys_to_delete)
```

### Create a Translation

```python
project_id = "your_project_id"
key_id = "your_key_id"
translation_content = "new_translation_content"
language_id = "optional_language_id"

new_translation = await texterify.create_translation(project_id, key_id, translation_content, language_id=language_id)
```

### Export a Project

```python
project_id = "your_project_id"
export_config_id = "your_export_config_id"
export_options = {
    "format": "json",
    "original": "true"
}

exported_project = await texterify.export_project(project_id, export_config_id, export_options)
```

### Import a File

```python
project_id = "your_project_id"
language_id = "your_language_id"
file_path = "path/to/your/file"

import_response = await texterify.import_project(project_id, language_id, file_path)
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.