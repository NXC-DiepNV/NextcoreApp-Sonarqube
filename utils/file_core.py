from .exception_core import ExceptionCore


class FileCore:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self):
        try:
            with open(self.file_path, 'r') as file:
                return file.readlines()
        except FileNotFoundError as e:
            raise ExceptionCore.raise_custom_exception(e)

    def write(self, content):
        try:
            # Write back the updated lines to the file
            with open(self.file_path, 'w') as file:
                file.writelines(content)
        except FileNotFoundError as e:
            raise ExceptionCore.raise_custom_exception(e)


class EnvFileCore(FileCore):

    def __init__(self, file_path):
        super().__init__(file_path)

    def update_line(self, key, new_value):
        try:
            lines = self.read()
            updated_lines = []
            key_found = False

            # Update the key's value if it exists
            for line in lines:
                if line.startswith(f"{key}="):
                    updated_lines.append(f"{key}={new_value}\n")
                    key_found = True
                else:
                    updated_lines.append(line)

            # If the key wasn't found, append it at the end
            if not key_found:
                updated_lines.append(f"{key}={new_value}\n")

            self.write(updated_lines)
        except Exception as e:
            print(f"An error occurred: {e}")
