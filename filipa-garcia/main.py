import click

from support import *


@click.command()
@click.option('--input_file', default='data_in.json', help='File with raw data')
@click.option('--window_size', default=10, help='Window size for moving range calculation')
@click.option('--output_file', default='', help='File to save data')
def open_file(input_file: str, window_size: int, output_file: str):
    """    """
    with open(input_file) as json_file:
        data = json.load(json_file)

    data_small = remove_columns(data)

    total = dict()
    total['entry'] = []
    for ma_data in moving_average(data_small, window_size):
        click.echo(ma_data)

        if output_file != '':
            save_to_file(ma_data, total, output_file)


if __name__ == '__main__':
    open_file()
