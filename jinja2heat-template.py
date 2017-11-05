import jinja2
import argparse
import sys


def jinja2_to_heat(template_file, output_file, arg_list):
    f = file(template_file)
    compiled_template = jinja2.Template(f.read())
    rendered_template = compiled_template.render({"arg_list": arg_list})
    tmp_file = file(output_file, mode="w")
    tmp_file.write(rendered_template)
    tmp_file.close
    print "output file: %s" % tmp_file.name


def genarater_list(number):
    arg_list = [arg for arg in range(1, number+1)]
    return arg_list


def command():
    parse = argparse.ArgumentParser()
    parse.add_argument("template_file")
    parse.add_argument('-o', default='tmp.hot', help="output file", dest="output_file", required=False)
    parse.add_argument('-c', dest="resource_num", type=int, required=True)
    return parse.parse_args()


args = command()
arg_list = genarater_list(args.resource_num)
jinja2_to_heat(args.template_file, args.output_file, arg_list)
