#!/bin/bash

# Generate HTML files for GitHub Pages

echo "Generating HTML files for GitHub Pages..."

# Create docs directory for GitHub Pages
mkdir -p docs

# Generate English resume HTML
echo "Converting English resume to HTML..."
pandoc xingqiangchen-en.tex -o docs/en-temp.html \
  --standalone \
  --metadata title="Xingqiang Chen - Resume" \
  --css=style.css \
  -V lang=en

# Add professional header to English resume
cat > docs/en.html << 'ENEOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Xingqiang Chen - Resume</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Professional Header -->
    <div class="resume-header">
        <div class="resume-photo">
            <img src="img/face.jpg" alt="Chen Xingqiang">
        </div>
        <div class="resume-info">
            <h1 style="margin: 0; border: none;">CHEN XINGQIANG</h1>
            <div class="subtitle">陈星强</div>
            <div class="resume-meta">
                <div class="resume-meta-item"><strong>Title:</strong> Product-Line Compiler Lead</div>
                <div class="resume-meta-item"><strong>Focus:</strong> AI Graph Compiler / Palladium Emulation / HW-SW Co-design</div>
                <div class="resume-meta-item"><strong>Degree:</strong> Ph.D. in Biophysics and Condensed Matter</div>
                <div class="resume-meta-item"><strong>Location:</strong> Hangzhou, China</div>
                <div class="resume-meta-item"><strong>Email:</strong> <a href="mailto:joy6677@outlook.com">joy6677@outlook.com</a></div>
                <div class="resume-meta-item"><strong>GitHub:</strong> <a href="https://github.com/chenxingqiang" target="_blank">@chenxingqiang</a></div>
            </div>
        </div>
    </div>
ENEOF

# Append the content (skip the header part)
tail -n +28 docs/en-temp.html | head -n -2 >> docs/en.html
echo "</body></html>" >> docs/en.html
rm docs/en-temp.html

# Generate Chinese resume HTML
echo "Converting Chinese resume to HTML..."
pandoc xingqiangchen-zn.tex -o docs/zn-temp.html \
  --standalone \
  --metadata title="陈星强 - 简历" \
  --css=style.css \
  -V lang=zh

# Add professional header to Chinese resume
cat > docs/zn.html << 'ZNEOF'
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>陈星强 - 简历</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Professional Header -->
    <div class="resume-header">
        <div class="resume-photo">
            <img src="img/face.jpg" alt="陈星强">
        </div>
        <div class="resume-info">
            <h1 style="margin: 0; border: none;">陈星强</h1>
            <div class="subtitle">CHEN XINGQIANG</div>
            <div class="resume-meta">
                <div class="resume-meta-item"><strong>职称:</strong> 产品线编译器负责人</div>
                <div class="resume-meta-item"><strong>专业方向:</strong> AI 图编译器 / Palladium 仿真验证 / 软硬件协同</div>
                <div class="resume-meta-item"><strong>学位:</strong> 博士（生物物理学与凝聚态物理）</div>
                <div class="resume-meta-item"><strong>位置:</strong> 杭州，中国</div>
                <div class="resume-meta-item"><strong>邮箱:</strong> <a href="mailto:joy6677@outlook.com">joy6677@outlook.com</a></div>
                <div class="resume-meta-item"><strong>GitHub:</strong> <a href="https://github.com/chenxingqiang" target="_blank">@chenxingqiang</a></div>
            </div>
        </div>
    </div>
ZNEOF

# Append the content (skip the header part)
tail -n +28 docs/zn-temp.html | head -n -2 >> docs/zn.html
echo "</body></html>" >> docs/zn.html
rm docs/zn-temp.html

# Generate Chinese adjusted resume HTML
echo "Converting Chinese adjusted resume to HTML..."
pandoc xingqiangchen-zn-adjust.tex -o docs/zn-adjust-temp.html \
  --standalone \
  --metadata title="陈星强 - 简历 (调整版)" \
  --css=style.css \
  -V lang=zh

# Add professional header to Chinese adjusted resume
cat > docs/zn-adjust.html << 'ZNAEOF'
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>陈星强 - 简历 (调整版)</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Professional Header -->
    <div class="resume-header">
        <div class="resume-photo">
            <img src="img/face.jpg" alt="陈星强">
        </div>
        <div class="resume-info">
            <h1 style="margin: 0; border: none;">陈星强</h1>
            <div class="subtitle">CHEN XINGQIANG</div>
            <div class="resume-meta">
                <div class="resume-meta-item"><strong>职称:</strong> 产品线编译器负责人</div>
                <div class="resume-meta-item"><strong>专业方向:</strong> AI 图编译器 / Palladium 仿真验证 / 软硬件协同</div>
                <div class="resume-meta-item"><strong>学位:</strong> 博士（生物物理学与凝聚态物理）</div>
                <div class="resume-meta-item"><strong>位置:</strong> 杭州，中国</div>
                <div class="resume-meta-item"><strong>邮箱:</strong> <a href="mailto:joy6677@outlook.com">joy6677@outlook.com</a></div>
                <div class="resume-meta-item"><strong>GitHub:</strong> <a href="https://github.com/chenxingqiang" target="_blank">@chenxingqiang</a></div>
            </div>
        </div>
    </div>
ZNAEOF

# Append the content (skip the header part)
tail -n +28 docs/zn-adjust-temp.html | head -n -2 >> docs/zn-adjust.html
echo "</body></html>" >> docs/zn-adjust.html
rm docs/zn-adjust-temp.html

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
                            <td>产品线编译器负责人 Product-Line Compiler Lead</td>
                        </tr>
                        <tr>
                            <td>专业方向:</td>
                            <td>AI 图编译器 / Palladium 仿真验证 / 软硬件协同</td>
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
        
        <p class="subtitle">🚀 AI Graph Compiler | Palladium Emulation | HW/SW Co-design | LLM Inference</p>
        
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
/* ============================================
   Academic Professional Style CSS
   Inspired by Tsinghua University Faculty Pages
   ============================================ */

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    line-height: 1.8;
    max-width: 1100px;
    margin: 0 auto;
    padding: 50px 30px;
    background: #f8f9fa;
    color: #2c3e50;
}

/* Professional Header with Photo */
.resume-header {
    display: flex;
    gap: 35px;
    margin-bottom: 40px;
    padding: 30px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    border-left: 5px solid #2c5aa0;
}

.resume-photo {
    flex-shrink: 0;
}

.resume-photo img {
    width: 180px;
    height: 180px;
    object-fit: cover;
    border-radius: 6px;
    border: 3px solid #2c5aa0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.resume-info {
    flex: 1;
}

.resume-info h1 {
    margin: 0 0 8px 0;
    font-size: 2.2em;
    color: #1a365d;
    font-weight: 600;
}

.resume-info .subtitle {
    font-size: 1.1em;
    color: #4a5568;
    margin-bottom: 20px;
    font-weight: 500;
}

.resume-meta {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 10px;
    padding: 15px;
    background: #f7fafc;
    border-radius: 6px;
    border-left: 3px solid #4299e1;
}

.resume-meta-item {
    color: #4a5568;
    font-size: 0.95em;
}

.resume-meta-item strong {
    color: #2d3748;
    font-weight: 600;
    margin-right: 8px;
}

/* Section Headers */
h1 {
    font-size: 2.2em;
    color: #1a365d;
    border-bottom: 3px solid #2c5aa0;
    padding-bottom: 12px;
    margin-top: 2.5em;
    margin-bottom: 1em;
    font-weight: 600;
}

h2 {
    font-size: 1.6em;
    color: #2c5aa0;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 10px;
    margin-top: 2.2em;
    margin-bottom: 1em;
    font-weight: 600;
}

h3 {
    font-size: 1.3em;
    color: #2d3748;
    margin-top: 1.8em;
    margin-bottom: 0.8em;
    padding: 12px 0 12px 18px;
    border-left: 4px solid #4299e1;
    background: #f7fafc;
    font-weight: 600;
}

h4 {
    font-size: 1.1em;
    color: #4a5568;
    margin-top: 1.5em;
    margin-bottom: 0.6em;
    font-weight: 600;
}

/* Section Containers */
.rSection, div[class*="Section"] {
    margin-bottom: 2.5em;
    padding: 25px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    border-left: 4px solid #2c5aa0;
}

/* Work Experience / Project Cards */
.rSubsection, div[class*="Subsection"] {
    margin-bottom: 2em;
    padding: 22px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #4299e1;
    border-radius: 6px;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.04);
}

.rSubsection:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
    transition: all 0.3s ease;
}

/* Lists */
ul {
    list-style-type: none;
    padding-left: 0;
    margin: 1em 0;
}

li {
    margin-bottom: 14px;
    padding-left: 28px;
    position: relative;
    line-height: 1.7;
    color: #4a5568;
}

li::before {
    content: "■";
    color: #4299e1;
    font-size: 0.7em;
    position: absolute;
    left: 8px;
    top: 8px;
}

/* Links */
a {
    color: #2c5aa0;
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: all 0.3s ease;
    font-weight: 500;
}

a:hover {
    color: #1a365d;
    border-bottom: 1px solid #2c5aa0;
}

/* Text Emphasis */
strong, b {
    color: #1a365d;
    font-weight: 600;
}

em, i {
    color: #2d3748;
    font-style: italic;
}

/* Code Blocks */
code {
    background: #edf2f7;
    padding: 3px 8px;
    border-radius: 4px;
    font-family: "Monaco", "Menlo", "Consolas", "Courier New", monospace;
    color: #c7254e;
    font-size: 0.9em;
}

/* Paragraphs */
p {
    margin-bottom: 1.2em;
    line-height: 1.8;
    color: #4a5568;
}

/* Tables (Academic Style) */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
    background: white;
}

table th {
    background: #2c5aa0;
    color: white;
    padding: 12px;
    text-align: left;
    font-weight: 600;
}

table td {
    padding: 10px 12px;
    border-bottom: 1px solid #e2e8f0;
}

table tr:hover {
    background: #f7fafc;
}

/* Horizontal Rules */
hr {
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 2.5em 0;
}

/* Blockquotes */
blockquote {
    margin: 1.5em 0;
    padding: 15px 20px;
    background: #f7fafc;
    border-left: 4px solid #4299e1;
    color: #4a5568;
    font-style: italic;
}

/* Print Styles */
@media print {
    body {
        background: white;
        max-width: 100%;
        padding: 0;
        font-size: 11pt;
    }
    
    .resume-header {
        page-break-inside: avoid;
        box-shadow: none;
        border: 1px solid #e2e8f0;
    }
    
    .rSection, .rSubsection {
        page-break-inside: avoid;
        box-shadow: none;
    }
    
    a {
        color: #000;
        text-decoration: underline;
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    body {
        padding: 25px 15px;
    }
    
    .resume-header {
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 20px;
    }
    
    .resume-photo img {
        width: 140px;
        height: 140px;
    }
    
    .resume-info h1 {
        font-size: 1.8em;
    }
    
    .resume-meta {
        grid-template-columns: 1fr;
    }
    
    h1 {
        font-size: 1.8em;
    }
    
    h2 {
        font-size: 1.4em;
    }
    
    h3 {
        font-size: 1.2em;
    }
    
    .rSection, .rSubsection {
        padding: 15px;
    }
}

/* Title Block (Pandoc Generated) */
#title-block-header {
    text-align: center;
    margin-bottom: 2em;
    padding: 30px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

#title-block-header .title {
    font-size: 2.5em;
    color: #1a365d;
    margin: 0;
    font-weight: 600;
}

/* Utility Classes */
.text-center {
    text-align: center;
}

.text-muted {
    color: #718096;
}

.mb-0 {
    margin-bottom: 0;
}

.mt-0 {
    margin-top: 0;
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

