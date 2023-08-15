import tomlkit
import json

class TomlConfig:
    def __init__(self, data, filename=None):
        """
        Class initializes, not called directly.
        """
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, TomlConfig(value))
            else:
                setattr(self, key, value)
        if filename : self.__file__ = filename

    @classmethod
    def load(cls, filename: str):
        """
        Load TOML data from the specified file and create a new instance of TomlConfig.

        Args:
            filename (str): The path of the TOML file to load.

        Returns:
            TomlConfig: An instance of TomlConfig containing the data from the file.

        Example:
            toml = TomlConfig.load('file.toml')
        """

        with open(filename, "a", encoding='utf-8'):
            pass
        with open(filename, "r", encoding='utf-8') as file:
            data = tomlkit.loads(file.read())
        return cls(data, filename=filename)

    def add_item(self, key: str, value):
        """
        Add a new item to the TOML data.

        Args:
            key (str): The key of the item to add, can be nested using dot notation.
            value (Any): The value of the item to add.

        Example:
            toml.add_item('section1.key1', 'value1')
        """
        keys = key.split('.')
        current_level = self
        for idx, k in enumerate(keys):
            if not hasattr(current_level, k):
                if idx == len(keys) - 1:
                    setattr(current_level, k, value)
                else:
                    setattr(current_level, k, TomlConfig({}))
            else:
                if idx == len(keys) - 1:
                    setattr(current_level, k, value)
            current_level = getattr(current_level, k)

    def remove_item(self, key: str):
        """
        Remove an item from the TOML data.

        This method allows you to remove an item (key-value pair) from the TOML data.

        Args:
            key (str): The key of the item to remove.

        Example:
            toml.remove_item('section1.key1')
        """
        keys = key.split('.')
        current_level = self
        for idx, k in enumerate(keys):
            if not hasattr(current_level, k):
                raise KeyError(f"Key '{key}' does not exist.")
            if idx == len(keys) - 1:
                delattr(current_level, k)
                break
            current_level = getattr(current_level, k)

    def update_item(self, key: str, value):
        """
        Update the value of an existing item in the TOML data.

        This method allows you to update the value of an existing item in the TOML data.

        Args:
            key (str): The key of the item to update.
            value (Any): The new value to set for the item.

        Raises:
            KeyError: If the specified key does not exist.

        Example:
            toml.section1.update_item('key1', 'new_value')
                toml.section1.key1 = old -> new_value
        """
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Key '{key}' does not exist.")

    def to_dict(self):
        data = {}
        for key, value in self.__dict__.items():
            if key == '__file__' or value is None:
                continue
            elif isinstance(value, TomlConfig):
                data[key] = value.to_dict()
            else:
                data[key] = value
        return data

    def save_to_file(self, filename):
        """
        Save TOML to a new file

        Args:
            filename (str): path to the TOML file

        Example:
            toml.save_to_file('filepath')
        """
        data = self.to_dict()

        with open(filename, "w", encoding='utf-8') as file:
            file.write(tomlkit.dumps(data))

    def add_items(self, items: list[dict]):
        """
        Add multiple items to the TOML data.

        This method allows you to add multiple key-value pairs to the TOML data at once.
        The items parameter should be a list of dictionaries, where each dictionary represents
        a key-value pair. Nested keys can be specified using dot notation.

        Args:
            items (list[dict]): A list of dictionaries representing the items to add.

        Example:
            toml.add_items([
                {"section1.key1": "value1"},
                {"section2.key2": "value2"},
                {"section3.key3": "value3"},
            ])
        """
        for item in items:
            for key, value in item.items():
                self.add_item(key, value)

    def save(self):
        """
        Save the modified TOML data back to the original file.

        Example:
            toml.save()
        """

        if self.__file__ is None:
            raise ValueError(
                "Original filename not available. Use save_to_file() instead.")
        self.save_to_file(self.__file__)
        
    def get(self, key:str):
        """
        Get the value of the given key.
        Return the dictionary of toml.data.key or its value.

        Args:
            key (str): The key to get.
            
        Example:
            tomlfile
            [data]
            key = 1
            key2 = 2
            
            python
            toml.data.get('key') >>> 1 
            toml.get('data')     >>> {'key': 1, 'key2': 2}
        """
        if hasattr(self, key):
            attr = getattr(self, key)
            if isinstance(attr, TomlConfig):
                return attr.__dict__
            else:return attr
        else:
            raise KeyError(f"Key '{key}' does not exist.")
        
    def to_json(self):
        """
        Converts Toml to JSON

        Returns:
            json_string:str
        """
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_json(cls, json_data:str):
        """
        Create a Toml object from JSON file

        Args:
            json_data (str): JSON file path
            
        Returns:
            Tomlconfig object
            
        Notice:
            With saving , using save_to_file().
        """
        with open(json_data,'r') as f:
            data = json.load(f)
            return cls(data)