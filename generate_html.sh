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
  --metadata title="陈星强 - 简历" \
  --css=style.css \
  -V lang=zh

# Generate Chinese adjusted resume HTML
echo "Converting Chinese adjusted resume to HTML..."
pandoc xingqiangchen-zn-adjust.tex -o docs/zn-adjust.html \
  --standalone \
  --metadata title="陈星强 - 简历 (调整版)" \
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
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", sans-serif;
            line-height: 1.6;
            max-width: 1200px;
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
        
        /* Professional Profile Section */
        .profile-section {
            display: flex;
            gap: 30px;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid #e2e8f0;
        }
        .profile-photo {
            flex-shrink: 0;
        }
        .profile-photo img {
            width: 200px;
            height: 200px;
            object-fit: cover;
            border-radius: 8px;
            border: 3px solid #667eea;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .profile-info {
            flex: 1;
        }
        .profile-info h1 {
            color: #2d3748;
            margin: 0 0 10px 0;
            font-size: 2.5em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .profile-info .name-en {
            font-size: 1.8em;
            color: #4a5568;
            margin-bottom: 15px;
        }
        .profile-details {
            background: #f7fafc;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .profile-details table {
            width: 100%;
            border-collapse: collapse;
        }
        .profile-details td {
            padding: 8px 0;
            vertical-align: top;
        }
        .profile-details td:first-child {
            font-weight: 600;
            color: #2d3748;
            width: 120px;
        }
        .profile-details td:last-child {
            color: #4a5568;
        }
        
        h2 {
            color: #667eea;
            text-align: center;
            margin: 30px 0 20px 0;
            font-size: 1.8em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.2em;
        }
        .versions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        .version-card {
            border: 2px solid #667eea;
            border-radius: 8px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
            background: linear-gradient(to bottom, #ffffff 0%, #f7fafc 100%);
        }
        .version-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            border-color: #764ba2;
        }
        .version-card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            margin: 5px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .btn:hover {
            background: #764ba2;
            transform: scale(1.05);
        }
        .btn-secondary {
            background: #48bb78;
        }
        .btn-secondary:hover {
            background: #38a169;
        }
        .contact {
            margin-top: 40px;
            padding: 25px;
            background: #f7fafc;
            border-radius: 8px;
            text-align: center;
            border-top: 3px solid #667eea;
        }
        .contact h3 {
            color: #2d3748;
            margin-bottom: 15px;
        }
        .contact a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        .contact a:hover {
            text-decoration: underline;
        }
        
        @media (max-width: 768px) {
            .profile-section {
                flex-direction: column;
                align-items: center;
            }
            .profile-photo img {
                width: 150px;
                height: 150px;
            }
            .profile-info h1 {
                font-size: 2em;
                text-align: center;
            }
            .profile-info .name-en {
                font-size: 1.4em;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Professional Profile Section -->
        <div class="profile-section">
            <div class="profile-photo">
                <img src="img/face.jpg" alt="Chen Xingqiang">
            </div>
            <div class="profile-info">
                <h1>陈星强</h1>
                <div class="name-en">CHEN XINGQIANG</div>
                <div class="profile-details">
                    <table>
                        <tr>
                            <td>职称 Title:</td>
                            <td>高级AI编译器工程师 Senior AI Compiler Engineer</td>
                        </tr>
                        <tr>
                            <td>专业方向:</td>
                            <td>大语言模型推理系统 / AI编译器 / 隐私保护机器学习</td>
                        </tr>
                        <tr>
                            <td>学位 Degree:</td>
                            <td>博士 Ph.D. (生物物理学与凝聚态物理)</td>
                        </tr>
                        <tr>
                            <td>位置 Location:</td>
                            <td>杭州，中国 Hangzhou, China</td>
                        </tr>
                        <tr>
                            <td>个人主页 Web:</td>
                            <td><a href="https://github.com/chenxingqiang" target="_blank">https://github.com/chenxingqiang</a></td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
        
        <p class="subtitle">🚀 LLM Inference Systems | AI Compiler | Privacy-Preserving ML | Recommendation Systems</p>
        
        <h2>📄 简历版本 Resume Versions</h2>
        
        <div class="versions">
            <div class="version-card">
                <h3>📄 English Resume</h3>
                <a href="en.html" class="btn">View HTML</a>
                <a href="xingqiangchen-en.pdf" class="btn btn-secondary" download>Download PDF</a>
            </div>
            
            <div class="version-card">
                <h3>📄 中文简历</h3>
                <a href="zn.html" class="btn">查看 HTML</a>
                <a href="xingqiangchen-zn.pdf" class="btn btn-secondary" download>下载 PDF</a>
            </div>
            
            <div class="version-card">
                <h3>📄 中文简历 (调整版)</h3>
                <a href="zn-adjust.html" class="btn">查看 HTML</a>
                <a href="xingqiangchen-zn-adjust.pdf" class="btn btn-secondary" download>下载 PDF</a>
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
    max-width: 1000px;
    margin: 0 auto;
    padding: 40px 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h2 {
    font-size: 1.8em;
    color: #667eea;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 8px;
    margin-top: 2em;
}

h3 {
    font-size: 1.4em;
    color: #4a5568;
    margin-top: 1.5em;
    padding: 10px 0;
    border-left: 4px solid #667eea;
    padding-left: 15px;
    background: #f7fafc;
}

/* 工作经历样式优化 */
.work-experience {
    margin-bottom: 2.5em;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    border-left: 4px solid #667eea;
}

/* 列表样式 */
ul {
    list-style-type: none;
    padding-left: 0;
}

li {
    margin-bottom: 12px;
    padding-left: 25px;
    position: relative;
}

li::before {
    content: "▸";
    color: #667eea;
    font-weight: bold;
    position: absolute;
    left: 5px;
}

/* 链接样式 */
a {
    color: #667eea;
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: all 0.3s ease;
}

a:hover {
    border-bottom: 1px solid #667eea;
}

strong, b {
    color: #2d3748;
    font-weight: 600;
    background: linear-gradient(to right, #ffd89b 0%, #19547b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

code {
    background: #edf2f7;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: "Monaco", "Menlo", "Courier New", monospace;
    color: #e53e3e;
}

/* 段落间距 */
p {
    margin-bottom: 1em;
    line-height: 1.8;
}

/* 水平线 */
hr {
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 2em 0;
}

/* 打印样式 */
@media print {
    body {
        background: white;
        max-width: 100%;
        padding: 0;
    }
    
    .work-experience {
        page-break-inside: avoid;
        box-shadow: none;
    }
}

/* 响应式设计 */
@media (max-width: 768px) {
    body {
        padding: 20px 10px;
    }
    
    h1 {
        font-size: 2em;
    }
    
    h2 {
        font-size: 1.5em;
    }
}
EOF

# Copy PDF files to docs directory
echo "Copying PDF files to docs directory..."
cp *.pdf docs/ 2>/dev/null || true

echo ""
echo "HTML files generated successfully!"
echo ""
echo "Generated files:"
echo "  - docs/index.html (Landing page)"
echo "  - docs/en.html (English resume)"
echo "  - docs/zn.html (Chinese resume)"
echo "  - docs/zn-adjust.html (Chinese adjusted resume)"
echo "  - docs/style.css (Stylesheet)"
echo "  - docs/*.pdf (PDF files)"
echo ""
echo "To enable GitHub Pages:"
echo "  1. Push these changes to GitHub"
echo "  2. Go to repository Settings > Pages"
echo "  3. Set source to 'main' branch and '/docs' folder"
echo "  4. Your resume will be available at: https://chenxingqiang.github.io/Resume/"

