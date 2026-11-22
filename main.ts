import { copyFileSync } from "fs";
import { join } from "path";

const src = join(import.meta.dirname, "out", "entry.png");
const destDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(destDir, "entry.png");

copyFileSync(src, dest);