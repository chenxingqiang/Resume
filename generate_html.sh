#!/bin/bash

# Generate HTML files for GitHub Pages

echo "Generating HTML files for GitHub Pages..."

# Create docs directory for GitHub Pages
mkdir -p docs

# Generate English resume HTML
echo "Converting English resume to HTML..."
pandoc xingqiangchen-en.tex -o docs/en.html \
  --standalone \
  --metadata title="Xingqiang Chen - Resume" \
  --css=style.css \
  -V lang=en

# Generate Chinese resume HTML
echo "Converting Chinese resume to HTML..."
pandoc xingqiangchen-zn.tex -o docs/zn.html \
  --standalone \
  --metadata title="陈兴强 - 简历" \
  --css=style.css \
  -V lang=zh

# Generate Chinese adjusted resume HTML
echo "Converting Chinese adjusted resume to HTML..."
pandoc xingqiangchen-zn-adjust.tex -o docs/zn-adjust.html \
  --standalone \
  --metadata title="陈兴强 - 简历 (调整版)" \
  --css=style.css \
  -V lang=zh

# Create landing page
cat > docs/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chen Xingqiang - Resume</title>
    <link rel="stylesheet" href="style.css">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
        }
        .versions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .version-card {
            border: 2px solid #667eea;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .version-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        }
        .version-card h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s ease;
        }
        .btn:hover {
            background: #764ba2;
        }
        .btn-secondary {
            background: #48bb78;
        }
        .btn-secondary:hover {
            background: #38a169;
        }
        .contact {
            margin-top: 40px;
            padding: 20px;
            background: #f7fafc;
            border-radius: 8px;
            text-align: center;
        }
        .contact a {
            color: #667eea;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Chen Xingqiang (陈兴强)</h1>
        <p class="subtitle">Senior AI Compiler Engineer | LLM Systems | Privacy-Preserving ML</p>
        
        <div class="versions">
            <div class="version-card">
                <h3>📄 English Resume</h3>
                <a href="en.html" class="btn">View HTML</a>
                <a href="../xingqiangchen-en.pdf" class="btn btn-secondary">Download PDF</a>
            </div>
            
            <div class="version-card">
                <h3>📄 中文简历</h3>
                <a href="zn.html" class="btn">查看 HTML</a>
                <a href="../xingqiangchen-zn.pdf" class="btn btn-secondary">下载 PDF</a>
            </div>
            
            <div class="version-card">
                <h3>📄 中文简历 (调整版)</h3>
                <a href="zn-adjust.html" class="btn">查看 HTML</a>
                <a href="../xingqiangchen-zn-adjust.pdf" class="btn btn-secondary">下载 PDF</a>
            </div>
        </div>
        
        <div class="contact">
            <h3>📫 Contact Information</h3>
            <p>
                <strong>Location:</strong> Hangzhou, China 杭州，中国<br>
                <strong>Phone:</strong> +86 150-0133-4125<br>
                <strong>Email:</strong> <a href="mailto:joy6677@outlook.com">joy6677@outlook.com</a><br>
                <strong>GitHub:</strong> <a href="https://github.com/chenxingqiang" target="_blank">@chenxingqiang</a>
            </p>
        </div>
    </div>
</body>
</html>
EOF

# Create CSS file
cat > docs/style.css << 'EOF'
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
    background: #f7fafc;
    color: #333;
}

h1, h2, h3, h4, h5, h6 {
    color: #2d3748;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

h1 {
    font-size: 2.5em;
    border-bottom: 3px solid #667eea;
    padding-bottom: 10px;
}

h2 {
    font-size: 1.8em;
    color: #667eea;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 5px;
}

a {
    color: #667eea;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

ul {
    list-style-type: disc;
    padding-left: 25px;
}

li {
    margin-bottom: 8px;
}

strong, b {
    color: #2d3748;
    font-weight: 600;
}

code {
    background: #edf2f7;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: "Monaco", "Menlo", "Courier New", monospace;
}

@media print {
    body {
        background: white;
        max-width: 100%;
        padding: 0;
    }
}
EOF

echo "HTML files generated successfully!"
echo ""
echo "Generated files:"
echo "  - docs/index.html (Landing page)"
echo "  - docs/en.html (English resume)"
echo "  - docs/zn.html (Chinese resume)"
echo "  - docs/zn-adjust.html (Chinese adjusted resume)"
echo "  - docs/style.css (Stylesheet)"
echo ""
echo "To enable GitHub Pages:"
echo "  1. Push these changes to GitHub"
echo "  2. Go to repository Settings > Pages"
echo "  3. Set source to 'main' branch and '/docs' folder"
echo "  4. Your resume will be available at: https://chenxingqiang.github.io/Resume/"

