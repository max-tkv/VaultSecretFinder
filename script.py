import click as click
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

param_list = '?list=true'
metadata_method = '/v1/secret/metadata/'
ui_method = '/ui/vault/secrets/secret/show/'
data_method = '/v1/secret/data/'


def search(host, token, vault_name, key, search_world):
    try:
        url_data = host + data_method + vault_name + key
        headers = {
            'x-vault-token': token
        }
        response = requests.get(url_data, headers=headers, verify=False)
        if response.status_code == 200:
            url_ui = host + ui_method + vault_name + key
            data = response.json()
            if search_world.lower() in str(data).lower():
                print(('\033[92m' + f"Найден в '{url_ui}'" + '\033[0m'))
            else:
                print(f"Не найден в '{url_ui}'")
        else:
            print(f"Ошибка запроса '{url_data}'. Статус код: {response.status_code}")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


def run(host, token, vault_name, search_world):
    try:
        url = host + metadata_method + vault_name + param_list
        headers = {
            'x-vault-token': token
        }
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            data = response.json()
            keys = data.get('data', {}).get('keys', [])
            for key in keys:
                if key[-1] == "/":
                    run(host, token, vault_name + key, search_world)
                    continue
                search(host, token, vault_name, key, search_world)
        else:
            print('\033[93m' + f"Ошибка запроса. Статус код: {response.status_code}" + '\033[0m')

    except Exception as e:
        print('\033[91m' + f"Произошла ошибка: {str(e)}" + '\033[0m')


@click.command()
@click.option('--directory', '-D',
              prompt=True,
              help='Корневую дерикторию для поиска')
@click.option('--host', '-H',
              default="http://localhost:8200",
              prompt=True,
              help='URL of the Vault')
@click.option('--search_world', '-S',
              type=str,
              prompt=True,
              help='Что нужно искать?')
@click.option('--token', '-T',
              type=str,
              prompt=True,
              help='Токен авторизации Vault')
def main(host, token, directory, search_world):
    run(host, token, directory, search_world)
    print("Поиск завершен!")
    input()


if __name__ == '__main__':
    main()
