#!/usr/bin/python

import sys
import re



if __name__ == "__main__":


    with open(sys.argv[1]) as f:
        lines = f.readlines()
    file_contents = "".join(lines)

    # strip comments.  They confuse our regex
    file_contents = re.sub(r"\\%", "MYPERCENT", file_contents)
    file_contents = re.sub(r"%.*", "", file_contents)
    file_contents = re.sub("MYPERCENT", "\\%", file_contents)
    
    # delete everything upto \document.  That's where the contents start
    exp = re.compile(r"^.*?\\document\s", re.MULTILINE|re.DOTALL)
    file_contents = re.sub(exp, "", file_contents, 1)
    
    # replace the old align methods
    mathmode = re.compile(r"\$\$(.*?)\$\$", re.MULTILINE|re.DOTALL)
    alignmode = re.compile(r"\$\$\s*\\align(.*?)\\endalign\s*\$\$", re.MULTILINE|re.DOTALL)
    alignatmode = re.compile(r"\$\$\s*\\alignat\s*\d+(.*?)\\endalignat\s*\$\$", re.MULTILINE|re.DOTALL)
    multlinemode = re.compile(r"\$\$\s*\\multline(.*?)\\endmultline\s*\$\$", re.MULTILINE|re.DOTALL)
    gathermode = re.compile(r"\$\$\s*\\gather(.*?)\\endgather\s*\$\$", re.MULTILINE|re.DOTALL)
    splitmode = re.compile(r"\$\$\s*\\split(.*?)\\endsplit\s*\$\$", re.MULTILINE|re.DOTALL)

    file_contents = re.sub(alignatmode, r"\\begin{align*}\1\\end{align*}", file_contents)
    file_contents = re.sub(alignmode, r"\\begin{align*}\1\\end{align*}", file_contents)
    file_contents = re.sub(multlinemode, r"\\begin{multline*}\1\\end{multline*}", file_contents)
    file_contents = re.sub(gathermode, r"\\begin{gather*}\1\\end{gather*}", file_contents)
    file_contents = re.sub(splitmode, r"\\[\\begin{split}\1\\end{split}\\]", file_contents)
    file_contents = re.sub(mathmode, r"\\[\1\\]", file_contents)

    # replace unested \hat\bold's
    exp = re.compile(r"\\hat\s*\\bold\s*((\\)*[a-zA-Z]+)", re.MULTILINE|re.DOTALL)
    file_contents = re.sub(exp, r"\\hat{\\bold \1}", file_contents)

    # put \tag\eqn in braces
    exp = re.compile(r"\\tag\\eqn", re.MULTILINE|re.DOTALL)
    file_contents = re.sub(exp, r"\\tag{\eqn}", file_contents)

    # remove all the \noexpand from the \outind blocks
    exp = re.compile(r"\\outind{(.*?)}")
    exp2 = re.compile(r"\\noexpand")
    file_contents = re.sub(exp, lambda match: "\\outind{" + re.sub(exp2, "", match.group(1)) + "}", file_contents)

    # encapsulate the \input ... exercises blocks
    exp = re.compile(r"\\input (chap.*\.ex.*)")
    file_contents = re.sub(exp, r"\\includeexercises{\1}", file_contents)
    
    # encapsulate the \input ... exercises blocks
    exp = re.compile(r"\\endchapter.*", re.MULTILINE|re.DOTALL)
    file_contents = re.sub(exp, r"\\endinput", file_contents)

    # convert to new matrix format
    file_contents = re.sub(r"\\matrix", r"\\begin{matrix}", file_contents)
    file_contents = re.sub(r"\\endmatrix", r"\\end{matrix}", file_contents)
    file_contents = re.sub(r"\\format.*?\\\\", "{}", file_contents) #put something there just so we don't leave blank lines which will upset latex
    # convert to new sb format
    file_contents = re.sub(r"\\Sb", r"_{\substack{", file_contents)
    file_contents = re.sub(r"\\endSb", r"}}", file_contents)
    
    # XXX really shouldn't do this, but it works for the evans book...
    file_contents = re.sub(r"\\noexpand", r"", file_contents)
    file_contents = re.sub(r"\\C([^a-zA-Z])", r"\\CC\1", file_contents)


    # stuff for converting the exercises
    # do this only on .ex? files
    if re.search(r"\.ex\d+", sys.argv[1]):
        # strip comments
        file_contents = re.sub(r"%.*", "", file_contents)

        # we're going to reinsert \endinput at the end of the file
        # so remove it if its already there
        file_contents = re.sub(r"\\endinput", "", file_contents)

        exp = re.compile(r".*?\\endsubhead", re.MULTILINE|re.DOTALL)
        file_contents = re.sub(exp, "", file_contents, 1)

        exers = file_contents.split("\\Exer")

        answer_exp = re.compile(r"\\answer(.*)", re.MULTILINE|re.DOTALL)
        def replace_answer_block(text):
            return re.sub(answer_exp, r"\n\\answer{\1\n}\n\n", text)

        exers = [replace_answer_block(b) for b in exers]

        if len(exers) > 1:
            exers[0] = exers[0] + "\n\n\\begin{enumerate}\n\n"
            exers[-1] = exers[-1] + "\n\n\\end{enumerate}"
        file_contents = "\item ".join(exers) + "\n\endinput"


    print(file_contents)
