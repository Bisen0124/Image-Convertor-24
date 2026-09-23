#!/usr/bin/env python3
import os
import re
import json

PAGES = [
    {
        "filename": "png-to-jpeg.html",
        "from_fmt": "PNG",
        "to_fmt": "JPEG",
        "target_js": "jpeg",
        "title": "PNG to JPEG Converter - 100% Free, Fast & No Login | Fast Image Convertor",
        "h1": "Free Online PNG to JPEG Converter",
        "description": "Convert PNG images to JPEG format instantly in your browser. 100% private, no login required, zero server uploads, lossless quality with fast batch processing.",
        "keywords": "png to jpeg converter, convert png to jpeg, png to jpeg online free, batch png to jpeg, no login image converter",
        "comparison_title": "PNG vs JPEG: Which Should You Choose?",
        "comparison_p": "PNG is a lossless image format ideal for transparent graphics, icons, and sharp text. JPEG is a lossy compressed format optimal for photographs and web images requiring small file sizes. Converting PNG to JPEG significantly reduces file size (often by 50% to 80%), making your web pages load much faster.",
        "faqs": [
            {
                "q": "How does converting PNG to JPEG reduce file size?",
                "a": "JPEG uses intelligent compression algorithms that discard subtle image data less noticeable to the human eye, reducing the byte size by up to 80% compared to uncompressed PNGs."
            },
            {
                "q": "What happens to PNG transparent backgrounds in JPEG?",
                "a": "JPEG does not support transparency. Our converter automatically fills transparent areas with a clean white background so your image looks natural and sharp."
            },
            {
                "q": "Do I need to sign in or create an account?",
                "a": "No. Fast Image Convertor requires no login, no signups, and no email. You can convert immediately with zero barriers."
            },
            {
                "q": "Are my PNG files uploaded to any server?",
                "a": "Never. All conversion happens directly in your browser using the HTML5 Canvas API. Your images never leave your computer or phone."
            }
        ]
    },
    {
        "filename": "png-to-jpg.html",
        "from_fmt": "PNG",
        "to_fmt": "JPG",
        "target_js": "jpg",
        "title": "PNG to JPG Converter - 100% Free, Fast & No Login | Fast Image Convertor",
        "h1": "Free Online PNG to JPG Converter",
        "description": "Quickly convert PNG to JPG online for free. No login needed, zero file uploads, ultra-fast client-side image converter with real-time preview.",
        "keywords": "png to jpg converter, convert png to jpg, free png to jpg, batch png to jpg, fast image converter",
        "comparison_title": "Why Convert PNG to JPG?",
        "comparison_p": "JPG is universally supported on every phone, computer, and web platform. Converting heavy PNG screenshots and graphics to JPG makes them much lighter to email, share on social media, or upload to websites.",
        "faqs": [
            {
                "q": "Is this PNG to JPG converter completely free?",
                "a": "Yes, 100% free with unlimited conversions and no daily quotas."
            },
            {
                "q": "Can I convert multiple PNG files to JPG at once?",
                "a": "Yes, you can drop dozens of PNG images and download them all together in a single ZIP file."
            },
            {
                "q": "How fast is the conversion?",
                "a": "Conversions happen in milliseconds because everything runs locally on your device hardware."
            },
            {
                "q": "Do I need to install any software or login?",
                "a": "No software installation and no account required. It runs instantly in Google Chrome, Safari, Firefox, and Edge."
            }
        ]
    },
    {
        "filename": "jpg-to-png.html",
        "from_fmt": "JPG",
        "to_fmt": "PNG",
        "target_js": "png",
        "title": "JPG to PNG Converter - 100% Free, Fast & No Login | Fast Image Convertor",
        "h1": "Free Online JPG to PNG Converter",
        "description": "Convert JPG images to lossless PNG format online for free. Fast, private, no signup or login required. Batch convert with instant download.",
        "keywords": "jpg to png converter, convert jpg to png, free jpg to png online, batch jpg to png, no login converter",
        "comparison_title": "JPG vs PNG: When to Convert to PNG?",
        "comparison_p": "Converting JPG to PNG provides a lossless container that prevents further compression degradation during repeated edits. PNG is also ideal when preparing graphics for digital printing, overlays, or graphic design software.",
        "faqs": [
            {
                "q": "Does converting JPG to PNG improve quality?",
                "a": "While it cannot restore information already lost during JPEG compression, converting to PNG stops any further loss of quality during editing and saving."
            },
            {
                "q": "Is there any limit on how many JPGs I can convert?",
                "a": "No limits! Convert as many JPG photos as you need with zero restrictions."
            },
            {
                "q": "Are my photos kept private?",
                "a": "Yes, 100% private. Files are processed locally on your device and are never sent to external servers."
            }
        ]
    },
    {
        "filename": "jpeg-to-png.html",
        "from_fmt": "JPEG",
        "to_fmt": "PNG",
        "target_js": "png",
        "title": "JPEG to PNG Converter - 100% Free, Fast & No Login | Fast Image Convertor",
        "h1": "Free Online JPEG to PNG Converter",
        "description": "Convert JPEG to PNG online in milliseconds. Free, instant, and private browser-based image conversion with no registration.",
        "keywords": "jpeg to png converter, convert jpeg to png, jpeg to png free, no login image converter",
        "comparison_title": "JPEG to PNG Conversion Benefits",
        "comparison_p": "Converting JPEG to PNG allows you to work with lossless raster graphics without generation loss. It is ideal for digital art, text graphics, and asset packaging.",
        "faqs": [
            {
                "q": "Can I paste an image directly to convert from JPEG to PNG?",
                "a": "Yes! Just drag and drop or browse your JPEG file to convert to PNG instantly."
            },
            {
                "q": "Is there any software to download?",
                "a": "No software needed. Fast Image Convertor runs entirely inside your existing web browser."
            }
        ]
    },
    {
        "filename": "webp-to-png.html",
        "from_fmt": "WebP",
        "to_fmt": "PNG",
        "target_js": "png",
        "title": "WebP to PNG Converter - 100% Free, Fast & No Login | Fast Image Convertor",
        "h1": "Free Online WebP to PNG Converter",
        "description": "Convert WebP images to PNG online for free. Preserves transparency, fast client-side processing, no login needed. Unlimited batch conversion.",
        "keywords": "webp to png converter, convert webp to png, webp to png online free, transparent webp to png, no login converter",
        "comparison_title": "WebP vs PNG: Compatibility & Transparency",
        "comparison_p": "While WebP is great for modern websites, older software, image editors (like older Photoshop), and some office applications cannot open WebP files. Converting WebP to PNG maintains transparency while providing universal compatibility across all programs.",
        "faqs": [
            {
                "q": "Does converting WebP to PNG keep transparent backgrounds?",
                "a": "Yes! Both WebP and PNG support alpha channel transparency, so your transparent backgrounds remain perfectly intact."
            },
            {
                "q": "Why do some apps fail to open WebP files?",
                "a": "WebP is a newer Google format. Many legacy desktop photo editors and print software only support PNG and JPG."
            }
        ]
    },
    {
        "filename": "png-to-webp.html",
        "from_fmt": "PNG",
        "to_fmt": "WebP",
        "target_js": "webp",
        "title": "PNG to WebP Converter - Compress Images Fast & No Login | Fast Image Convertor",
        "h1": "Free Online PNG to WebP Converter",
        "description": "Convert PNG to Google WebP format online. Reduce image file sizes by up to 70% while keeping transparency. 100% private, no signup required.",
        "keywords": "png to webp converter, convert png to webp, compress png to webp, webp image converter, fast webp conversion",
        "comparison_title": "Why WebP is Better for Websites than PNG",
        "comparison_p": "WebP images are on average 26% smaller than PNGs while retaining full transparency and visual crispness. Converting your website PNG assets to WebP dramatically improves Google PageSpeed scores, Core Web Vitals, and SEO rankings.",
        "faqs": [
            {
                "q": "How much file size do I save converting PNG to WebP?",
                "a": "Most users see 40% to 75% file size reduction without noticeable loss in visual clarity."
            },
            {
                "q": "Does WebP support transparency like PNG?",
                "a": "Yes, WebP supports full 8-bit alpha transparency while compressing much smaller than PNG."
            }
        ]
    },
    {
        "filename": "webp-to-jpg.html",
        "from_fmt": "WebP",
        "to_fmt": "JPG",
        "target_js": "jpg",
        "title": "WebP to JPG Converter - 100% Free, Fast & No Login | Fast Image Convertor",
        "h1": "Free Online WebP to JPG Converter",
        "description": "Convert WebP images to standard JPG format in seconds. 100% browser-based, no login required, zero server uploads. Free bulk conversions.",
        "keywords": "webp to jpg converter, convert webp to jpg, webp to jpeg online, batch webp to jpg, free image converter",
        "comparison_title": "Why Convert WebP to JPG?",
        "comparison_p": "Downloaded images from the web often save as .webp, which can be difficult to view or insert into presentations, Word documents, or older software. Converting WebP to standard JPG gives you immediate compatibility everywhere.",
        "faqs": [
            {
                "q": "Can I open the converted JPG file anywhere?",
                "a": "Yes, JPG is the universal standard supported by 100% of devices, operating systems, and programs."
            },
            {
                "q": "Is there any delay or queue when converting?",
                "a": "Zero wait time! Processing happens locally on your computer in milliseconds."
            }
        ]
    },
    {
        "filename": "jpg-to-webp.html",
        "from_fmt": "JPG",
        "to_fmt": "WebP",
        "target_js": "webp",
        "title": "JPG to WebP Converter - Reduce Image Size Fast & No Login | Fast Image Convertor",
        "h1": "Free Online JPG to WebP Converter",
        "description": "Convert JPG to next-gen WebP images online for free. Slash photo file size by 30-50% for faster website loading. No login, 100% private.",
        "keywords": "jpg to webp converter, convert jpg to webp, compress jpg to webp, next-gen image converter",
        "comparison_title": "Boost Website Speed with WebP",
        "comparison_p": "Google recommends using next-gen image formats like WebP to speed up page load times. Converting your JPG photos to WebP reduces bandwidth usage by 30% or more with zero perceptible quality difference.",
        "faqs": [
            {
                "q": "Will converting JPG to WebP help my SEO ranking?",
                "a": "Yes! Google explicitly uses page speed and Core Web Vitals as ranking factors. Lighter WebP images improve your website speed score."
            },
            {
                "q": "Can I adjust WebP compression quality?",
                "a": "Yes, use our real-time quality slider to balance file size and visual fidelity."
            }
        ]
    },
    {
        "filename": "heic-to-jpg.html",
        "from_fmt": "HEIC",
        "to_fmt": "JPG",
        "target_js": "jpg",
        "title": "HEIC to JPG Converter - Convert iPhone Photos Fast (No Login) | Fast Image Convertor",
        "h1": "Free Online HEIC to JPG Converter",
        "description": "Convert Apple iPhone HEIC/HEIF photos to standard JPG format online for free. 100% private in-browser conversion, no login required, bulk batch support.",
        "keywords": "heic to jpg converter, convert heic to jpg, iphone photo to jpg, heif to jpg online free, batch heic to jpg",
        "comparison_title": "Converting iPhone HEIC Photos to JPG",
        "comparison_p": "iPhones and iPads take photos in the HEIC format by default to save storage space. However, Windows PCs, Android devices, and many online forms cannot open HEIC files. Our converter transforms HEIC photos into standard JPGs immediately.",
        "faqs": [
            {
                "q": "What is a HEIC file?",
                "a": "HEIC (High Efficiency Image Container) is the default image format used by Apple iOS on iPhones and iPads."
            },
            {
                "q": "Why convert HEIC to JPG?",
                "a": "JPG is compatible with Windows, Android, websites, and social media platforms that do not recognize HEIC."
            }
        ]
    },
    {
        "filename": "heic-to-png.html",
        "from_fmt": "HEIC",
        "to_fmt": "PNG",
        "target_js": "png",
        "title": "HEIC to PNG Converter - 100% Free, Fast & No Login | Fast Image Convertor",
        "h1": "Free Online HEIC to PNG Converter",
        "description": "Convert iPhone HEIC photos to lossless PNG format online for free. Private browser-based processing, no signup required, instant download.",
        "keywords": "heic to png converter, convert heic to png, iphone photo to png, free heic converter",
        "comparison_title": "HEIC to PNG for High Fidelity",
        "comparison_p": "Convert your iPhone camera shots into lossless PNG images for digital editing, graphic design, or presentation creation without compression artifacts.",
        "faqs": [
            {
                "q": "Can I convert HEIC photos directly on my phone?",
                "a": "Yes! Our web application works smoothly on iPhones, Android phones, Mac, and Windows computers."
            }
        ]
    },
    {
        "filename": "svg-to-png.html",
        "from_fmt": "SVG",
        "to_fmt": "PNG",
        "target_js": "png",
        "title": "SVG to PNG Converter - High Quality, Fast & No Login | Fast Image Convertor",
        "h1": "Free Online SVG to PNG Converter",
        "description": "Convert vector SVG graphics to raster PNG images online for free. Transparent background preserved, ultra-fast client-side conversion, no login required.",
        "keywords": "svg to png converter, convert svg to png, vector to png online free, transparent svg to png",
        "comparison_title": "Converting Vector SVG to Raster PNG",
        "comparison_p": "SVG is XML vector code that scales infinitely, while PNG is a high-resolution pixel raster format. Converting SVG to PNG allows you to easily embed vector logos and illustrations into social media posts, slide decks, and documents that do not support SVG.",
        "faqs": [
            {
                "q": "Does SVG to PNG retain transparency?",
                "a": "Yes! The resulting PNG will retain the transparent background of your SVG graphic."
            }
        ]
    },
    {
        "filename": "jpeg-to-webp.html",
        "from_fmt": "JPEG",
        "to_fmt": "WebP",
        "target_js": "webp",
        "title": "JPEG to WebP Converter - 100% Free, Fast & No Login | Fast Image Convertor",
        "h1": "Free Online JPEG to WebP Converter",
        "description": "Convert JPEG images to next-gen WebP format online. Reduce image file size by up to 75% while maintaining visual crispness. 100% private, no signup, no login required.",
        "keywords": "jpeg to webp converter, convert jpeg to webp, free jpeg to webp, compress jpeg to webp, no login image converter",
        "comparison_title": "JPEG vs WebP: Why Convert to WebP?",
        "comparison_p": "WebP was created by Google as a high-performance modern replacement for JPEG. WebP achieves 25% to 34% smaller file sizes than comparable JPEG images at identical visual quality. Converting your JPEG photos to WebP speeds up website loading, saves visitor mobile data, and directly boosts Google Core Web Vitals and SEO rankings.",
        "faqs": [
            {
                "q": "How much file size do I save converting JPEG to WebP?",
                "a": "Most users experience 25% to 50% file size reduction without any noticeable loss in image sharpness."
            },
            {
                "q": "Does WebP work across all modern web browsers?",
                "a": "Yes! WebP is fully supported on Google Chrome, Apple Safari, Mozilla Firefox, Microsoft Edge, and mobile browsers."
            },
            {
                "q": "Do I need to create an account or login to convert?",
                "a": "No login, signup, or email is required. Conversions are completely free with zero barriers."
            },
            {
                "q": "Are my photos uploaded to a third-party server?",
                "a": "Never. All image processing runs locally in your browser hardware using the HTML5 Canvas API."
            }
        ]
    },
    {
        "filename": "webp-to-jpeg.html",
        "from_fmt": "WebP",
        "to_fmt": "JPEG",
        "target_js": "jpeg",
        "title": "WebP to JPEG Converter - 100% Free, Fast & No Login | Fast Image Convertor",
        "h1": "Free Online WebP to JPEG Converter",
        "description": "Convert WebP images to standard JPEG format online for free. Instant client-side conversion, no login required, zero server uploads. Unlimited bulk processing.",
        "keywords": "webp to jpeg converter, convert webp to jpeg, free webp to jpeg online, bulk webp to jpeg, fast image converter",
        "comparison_title": "Why Convert WebP to JPEG?",
        "comparison_p": "While WebP is common on modern websites, many older desktop photo editors, Microsoft Office versions, email clients, and digital print kiosks cannot open .webp files. Converting WebP to JPEG gives you universal compatibility everywhere.",
        "faqs": [
            {
                "q": "Will the converted JPEG open on any computer or phone?",
                "a": "Yes! JPEG is universally recognized by 100% of devices, apps, operating systems, and photo viewers worldwide."
            },
            {
                "q": "Can I convert multiple WebP files at once?",
                "a": "Yes! You can drop multiple WebP images simultaneously and download them all together in a single ZIP file."
            },
            {
                "q": "Is there any delay or queue when converting?",
                "a": "Zero waiting time! Processing happens in milliseconds directly on your device."
            },
            {
                "q": "Is there any software to install or account to register?",
                "a": "No installation and no registration. Fast Image Convertor works immediately in your browser."
            }
        ]
    },
    {
        "filename": "heic-to-jpeg.html",
        "from_fmt": "HEIC",
        "to_fmt": "JPEG",
        "target_js": "jpeg",
        "title": "HEIC to JPEG Converter - Convert iPhone Photos Fast & No Login | Fast Image Convertor",
        "h1": "Free Online HEIC to JPEG Converter",
        "description": "Convert Apple iPhone HEIC/HEIF photos to standard JPEG online for free. 100% private in-browser conversion, no login required, high-resolution bulk photo processing.",
        "keywords": "heic to jpeg converter, convert heic to jpeg, iphone photo to jpeg, heif to jpeg free, batch heic to jpeg",
        "comparison_title": "Why Convert iPhone HEIC Photos to JPEG?",
        "comparison_p": "Apple iOS devices capture photos in HEIC format to save storage. However, Windows PCs, older Macs, Android devices, and many online submission portals cannot display HEIC. Converting HEIC to JPEG gives you universal compatibility with zero hassle.",
        "faqs": [
            {
                "q": "Can I convert iPhone photos on my PC or phone?",
                "a": "Yes, Fast Image Convertor works directly on any browser on Windows, Mac, iOS, Android, and Linux."
            },
            {
                "q": "Do I need to install any software or app?",
                "a": "No installation and no login required. It runs straight inside your web browser."
            },
            {
                "q": "Does converting HEIC to JPEG lose photo metadata or clarity?",
                "a": "Our conversion engine maintains high fidelity and converts your photos in crisp detail."
            },
            {
                "q": "Is it really free?",
                "a": "Yes, 100% free with no hidden charges or subscriptions."
            }
        ]
    }
]

def generate():
    root = "/Users/sandeep/Documents/GitHub/Image-Convertor-24"
    os.chdir(root)

    with open("index.html", "r", encoding="utf-8") as f:
        base_html = f.read()

    sitemap_urls = [
        ("https://fastimageconvertor.com/", "1.0"),
        ("https://fastimageconvertor.com/privacy-policy.html", "0.5"),
        ("https://fastimageconvertor.com/terms.html", "0.5")
    ]

    for p in PAGES:
        html = base_html

        # 1. Title & Meta
        html = re.sub(r"<title>.*?</title>", f"<title>{p['title']}</title>", html)
        html = re.sub(r'<meta name="description"\s+content=".*?">', f'<meta name="description"\n      content="{p["description"]}">', html)
        html = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="https://fastimageconvertor.com/{p["filename"]}">', html)
        html = re.sub(r'<meta property="og:title"\s+content=".*?">', f'<meta property="og:title"\n      content="{p["title"]}">', html)
        html = re.sub(r'<meta property="og:description"\s+content=".*?">', f'<meta property="og:description"\n      content="{p["description"]}">', html)
        html = re.sub(r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="https://fastimageconvertor.com/{p["filename"]}">', html)

        # 2. Target H1 and Subhead (omit data-i18n to keep SEO-specific copy on load)
        html = re.sub(r'<h1 data-i18n="imgH1">.*?</h1>', f'<h1>{p["h1"]}</h1>', html)
        html = re.sub(r'<p class="sub" data-i18n="imgSub">.*?</p>', f'<p class="sub">{p["description"]}</p>', html)

        # 3. Dropzone text
        dz_text = f"Drag & drop {p['from_fmt']} or <b>click to convert to {p['to_fmt']}</b>"
        html = re.sub(r'<div class="dz-title" data-i18n="imgDzTitle">.*?</div>', f'<div class="dz-title">{dz_text}</div>', html)

        # 4. Preset currentGlobalFormat
        html = html.replace("let currentGlobalFormat = 'jpeg';", f"let currentGlobalFormat = '{p['target_js']}';")
        html = html.replace("let currentGlobalFormat = 'jpg';", f"let currentGlobalFormat = '{p['target_js']}';")

        # 5. Insert comparison text at beginning of SEO article
        comparison_block = f"""
      <h2>{p['comparison_title']}</h2>
      <p>{p['comparison_p']}</p>
"""
      # Insert before first h2 in seo-article
        html = html.replace('<h2 data-i18n="seoImgH2_1">', comparison_block + '      <h2 data-i18n="seoImgH2_1">')

        # 6. Structured Data FAQ Schema
        faq_entities = []
        for faq in p["faqs"]:
            faq_entities.append({
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["a"]
                }
            })
        faq_schema_str = json.dumps({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities
        }, indent=2)
        html = html.replace('</head>', f'<script type="application/ld+json">\n{faq_schema_str}\n</script>\n</head>')

        # 7. Structured Data BreadcrumbList Schema
        breadcrumb_schema = json.dumps({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://fastimageconvertor.com/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": p["h1"],
                    "item": f"https://fastimageconvertor.com/{p['filename']}"
                }
            ]
        }, indent=2)
        html = html.replace('</head>', f'<script type="application/ld+json">\n{breadcrumb_schema}\n</script>\n</head>')

        with open(p["filename"], "w", encoding="utf-8") as out_f:
            out_f.write(html)
        print(f"Generated {p['filename']} matching original backup UI exactly!")
        sitemap_urls.append((f"https://fastimageconvertor.com/{p['filename']}", "0.9"))

    # Generate clean sitemap.xml
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for loc, prio in sitemap_urls:
        sitemap_lines.append(f"""  <url>
    <loc>{loc}</loc>
    <changefreq>weekly</changefreq>
    <priority>{prio}</priority>
  </url>""")
    sitemap_lines.append('</urlset>\n')

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_lines))
    print("Updated sitemap.xml (all image pages, 0 video pages)")

    # Generate clean robots.txt
    robots_content = """User-agent: *
Allow: /

Sitemap: https://fastimageconvertor.com/sitemap.xml
"""
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)
    print("Updated robots.txt")

if __name__ == "__main__":
    generate()
