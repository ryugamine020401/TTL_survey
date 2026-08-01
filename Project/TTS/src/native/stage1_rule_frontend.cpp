#include <cstdio>
#include <fstream>
#include <iterator>
#include <string>

#include "darray.h"
#include "klatt.h"
#include "tts.h"

extern FILE *gFrameDump;

int main(int argc, char **argv)
{
    if (argc != 3)
    {
        std::fprintf(stderr, "usage: stage1_rule_frontend TEXT_FILE CONTROL_CSV\n");
        return 2;
    }

    std::ifstream input(argv[1], std::ios::binary);
    if (!input)
    {
        std::fprintf(stderr, "cannot open input text\n");
        return 3;
    }
    std::string text((std::istreambuf_iterator<char>(input)), std::istreambuf_iterator<char>());
    if (text.empty())
    {
        std::fprintf(stderr, "input text is empty\n");
        return 4;
    }

    darray phones;
    darray elements;
    xlate_string(text.c_str(), &phones);

    klatt synth;
    synth.init(1200, 10.0f, 0.25f, KW_SAW);
    klatt::phone_to_elm(phones.getData(), phones.getSize(), &elements);
    synth.initsynth(elements.getSize(), reinterpret_cast<unsigned char *>(elements.getData()));

    gFrameDump = std::fopen(argv[2], "wb");
    if (!gFrameDump)
    {
        std::fprintf(stderr, "cannot open control output\n");
        return 5;
    }

    short buffer[32768];
    while (synth.synth(32768, buffer) >= 0)
    {
    }

    std::fclose(gFrameDump);
    gFrameDump = NULL;
    return 0;
}
