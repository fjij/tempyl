#!/usr/bin/env python3

import sys
import json
from string import Template

def code_error(message, line, filename):
  msg = "\n" +"    "+"Error @ "+filename+":"+str(line[1])+"\n" +"    "+message+"\n" +"\n" +"    "+"HERE:"+"\n" +"    "+line[0]+"\n"
  sys.exit(msg)

def arg_error(message):
  msg = "\n" +"    "+"Error\n" +"    "+message+"\n"+"\n"+"    USAGE:\n    python3 tempyl.py template_file data_file output_file\n"
  sys.exit(msg)

def entemplate(lines, data):
  out = []
  for line in lines:
    (out.append(Template(line[0]).safe_substitute(data, self=data)), line[1])
  return out

def assign_scope(lines):
  out = []
  scoped_lines = []
  scope = ""
  enter_line = None
  depth = 0
  for line in lines:
    if line[0].strip().startswith('##'):
      # Line starts with scope modifier
      token = line[0].strip()[2:].strip()
      if (token != ""):
        # The target scope is defined
        if (scope == ""):
          # Enscope if we are not yet
          out.append((scope, scoped_lines, enter_line))
          scoped_lines=[]
          enter_line=line
          scope = token
        else:
          # Otherwise increase depth
          scoped_lines.append(line)
          depth += 1
      else:
        # There is no target scope, thus we are de-scoping
        if (scope == ""):
          # We are already unscoped, this should not be the case
          code_error("Cannot unscope any further!", line, template_fname)
        elif (depth == 0):
          # We are at depth zero, exit current scope
          out.append((scope, scoped_lines, enter_line))
          scoped_lines=[]
          scope = token
          enter_line = None
        else:
          # Decrease depth
          scoped_lines.append(line)
          depth -= 1
    else:
      # Add to sc
      scoped_lines.append(line)
  # Add final scoped lines
  out.append((scope, scoped_lines, enter_line))
  return out

def render_lines(lines, data):
  out_lines = []
  for (scope, scoped_lines, error_line) in assign_scope(lines):
    if scope == "":
      out_lines.extend(entemplate(scoped_lines, data))
    elif scope not in data.keys():
      # this should not be the case
      code_error("Key '"+scope+"' could not be found in the current scope.", 
        error_line, template_fname)
    elif type(data[scope]) is list:
      # List Repetition
      #.begin functionality
      begin = ""
      begin_key = scope + '.begin'
      if begin_key in data.keys():
        begin = data[begin_key]
      #.separator functionality
      separator = "\n"
      sep_key = scope + '.separator'
      if sep_key in data.keys():
        separator = data[sep_key]
      #.end functionality
      end = "\n"
      end_key = scope + '.end'
      if end_key in data.keys():
        end = data[end_key]
        
      out_lines.append(begin)
      for item in data[scope]:
        if type(item) is not dict or '.disabled' not in item.keys():
          out_lines.extend(render_lines(scoped_lines, item))
          out_lines[-1] = out_lines[-1].rstrip('\n')
          out_lines[-1] += separator
      out_lines[-1] = out_lines[-1].rstrip(separator)
      out_lines[-1] += end
    else:
      out_lines.extend(render_lines(scoped_lines, data[scope]))
  return out_lines

if (len(sys.argv) == 4):
  _, template_fname, data_fname, out_fname = sys.argv
else:
  arg_error("An incorrect number of arguments was provided")

try:
  with open(template_fname, 'r') as f:
    in_lines = map(lambda l: (l[1],l[0]+1), enumerate(f.readlines()))
except:
  arg_error("Could not load file: "+template_fname)

try:
  with open(data_fname, 'r') as f:
    json_data = json.load(f)
except:
  arg_error("Could not load file: "+data_fname)


out_lines = render_lines(in_lines, json_data)

try:
  with open(out_fname, 'w') as f:
    f.writelines(out_lines)
except:
  arg_error("Could not write to file: "+out_fname)
  
