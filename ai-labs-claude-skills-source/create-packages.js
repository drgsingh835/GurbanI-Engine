import fs from "fs";
import path from "path";

const skillsDir = path.resolve("packages/skills"); // ✅ correct path
const folders = fs.readdirSync(skillsDir);

for (const folder of folders) {
  const skillPath = path.join(skillsDir, folder);
  const stat = fs.statSync(skillPath);

  // Skip non-folders or files like .skill
  if (!stat.isDirectory()) continue;

  const pkgFile = path.join(skillPath, "package.json");
  if (fs.existsSync(pkgFile)) {
    console.log(`⏩ Skipping ${folder} (package.json already exists)`);
    continue;
  }

  // Create default package.json
  const pkg = {
    name: `@ai-labs-claude-skills/${folder}`,
    version: "1.0.0",
    description: `Claude AI skill: ${folder}`,
    main: "index.js",
    files: ["."],
    license: "MIT",
    author: "AI Labs"
  };

  fs.writeFileSync(pkgFile, JSON.stringify(pkg, null, 2));
  console.log(`✅ Created package.json for ${folder}`);
}

console.log("\n✨ All missing package.json files generated!");
