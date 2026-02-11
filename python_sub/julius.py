import re, asyncio


cmd = [
    r"/home/syamucat/Desktop/sotuken/main/julius/julius",
    "-C",
    r"/home/syamucat/Desktop/sotuken/main/julius/main.jconf",
]

pattern_pass1best = re.compile(r"pass1_best:\s*(.*?)$", re.MULTILINE)
pattern_sentence1 = re.compile(r"sentence1:\s*<s>\s*(.*?)\s*</s>")
pattern_cmscore1 = re.compile(r"cmscore1:\s*(\S+)\s*(\S+).*$", re.MULTILINE)


def extraction(text):
    data = {}
    # print(text)
    match = pattern_pass1best.search(text)
    if match:
        data["pass1_best"] = match.group(1)

    match = pattern_sentence1.search(text)
    if match:
        data["sentence1"] = match.group(1)

    match = pattern_cmscore1.search(text)
    if match:
        data["cmscore1"] = match.group(2)

    print(data)
    return data


class Process:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def read_process(self):
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        print("Listening...")
        sentence = ""

        try:
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                line = line.decode(errors="ignore")  # .rstrip()
                print(line)
                sentence += line
                if ("score1:" in line) and (not "cmscore1:" in line):
                    data = extraction(sentence)
                    await self.queue.put(data)
                    sentence = ""

        except asyncio.CancelledError:
            raise

        finally:
            if process.returncode is None:
                process.terminate()
                await process.wait()
