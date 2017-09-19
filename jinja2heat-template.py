import jinja2
import sys
f = open(sys.argv[1])
heat_template = f.read()
xlist = [x for x in range(250)]
print heat_template
print "============================="
compiled_template = jinja2.Template(heat_template)
print compiled_template
rendered_template = compiled_template.render({"xlist": xlist})
tmp_file = file("tmp.hot", mode="w")
tmp_file.write(rendered_template)
tmp_file.close
