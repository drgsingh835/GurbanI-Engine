import fs from "fs";
import path from "path";

const skillsDir = path.resolve("packages/skills");
const folders = fs.readdirSync(skillsDir);

for (const folder of folders) {
  const skillPath = path.join(skillsDir, folder);
  const stat = fs.statSync(skillPath);

  // Skip non-folders
  if (!stat.isDirectory()) continue;

  const indexFile = path.join(skillPath, "index.js");

  // Skip if already exists
  if (fs.existsSync(indexFile)) {
    console.log(`⏭️ Skipping ${folder} (index.js already exists)`);
    continue;
  }

  // Auto-create default template
  const template = `export default async function ${folder.replace(/[-.]/g, "_")}(input) {
  console.log("🧠 Running skill: ${folder}");
  
  // TODO: implement actual logic for this skill
  return {
    message: "Skill '${folder}' executed successfully!",
    input
  };
}
`;

  fs.writeFileSync(indexFile, template);
  console.log(`✅ Created index.js for ${folder}`);
}

console.log("\n✨ All missing index.js files generated!");
