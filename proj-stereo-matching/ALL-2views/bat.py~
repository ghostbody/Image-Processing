import os

def run(stero_pro, LeftImage, RightImage):
    os.system("%s %s %s left" % (stero_pro, LeftImage, RightImage))
    os.system("%s %s %s right" % (stero_pro, LeftImage, RightImage))

def runRes():
    for each in os.listdir("./tests/"):
        run("./stero", "./tests/%s/view1.png" % each, "./tests/%s/view5.png" % each)
        os.system("mkdir ./result/%s" % each)
        os.system("mv ./Left.png ./result/%s/Left.png" % each)
        os.system("mv ./Right.png ./result/%s/Right.png" % each)
        os.system("cp ./tests/%s/disp1.png ./result/%s/GroudTruthLeft.png" % (each, each))
        os.system("cp ./tests/%s/disp5.png ./result/%s/GroudTruthRight.png" % (each, each))

def runEval():
    for each in os.listdir("./result/"):
        os.system("./evaluate ./result/%s/Left.png ./result/%s/GroudTruthLeft.png %s" % (each, each, each))
        os.system("./evaluate ./result/%s/Right.png ./result/%s/GroudTruthRight.png %s" % (each, each, each))

def main():
    os.system("make")
    runRes()
    runEval()

if __name__ == '__main__':
    main()
