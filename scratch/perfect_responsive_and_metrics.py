# -*- coding: utf-8 -*-
from pathlib import Path

tmpl_path = Path(r"c:\Users\win\Desktop\cephane-fiyat-takip\src\fiyat_takip_sistemi\api\templates\index.html")

# Let's inspect index.html and redesign the CSS and layout for bulletproof responsiveness and millimeter-perfect proportionality.
code = tmpl_path.read_text(encoding="utf-8")

# Let's write the complete, perfected HTML template
new_html = r"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cep-Hane Teknoloji — Pazaryeri Fiyat & Rekabet Karar Destek Merkezi</title>
    <!-- Google Fonts: Plus Jakarta Sans & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;

            /* Surface Colors */
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --bg-subtle: #f1f5f9;
            --border-subtle: #e2e8f0;
            --border-strong: #cbd5e1;

            /* Brand & Neutral Texts */
            --text-main: #0f172a;
            --text-muted: #64748b;
            --text-light: #94a3b8;

            /* State Colors */
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --primary-light: #eff6ff;

            --emerald: #059669;
            --emerald-bg: #ecfdf5;
            --emerald-border: #a7f3d0;

            --rose: #e11d48;
            --rose-bg: #fff1f2;
            --rose-border: #fecdd3;

            --amber: #d97706;
            --amber-bg: #fffbeb;
            --amber-border: #fde68a;

            --indigo: #4f46e5;
            --indigo-bg: #eef2ff;

            /* Shadows */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-sans);
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            overflow-x: hidden;
        }

        /* -------------------------------------------------------------
           1. TOPBAR (Responsive & Millimeter Aligned)
           ------------------------------------------------------------- */
        .topbar-enterprise {
            background: #090d16;
            color: #e2e8f0;
            font-size: 0.75rem;
            padding: 0.5rem 1.25rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
            gap: 0.5rem;
        }

        .topbar-left {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            flex-wrap: wrap;
        }

        .topbar-right {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            flex-wrap: wrap;
        }

        .topbar-badge {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: #ffffff;
            font-weight: 700;
            font-size: 0.65rem;
            padding: 0.2rem 0.5rem;
            border-radius: 9999px;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .topbar-company {
            font-weight: 600;
            color: #f8fafc;
            display: flex;
            align-items: center;
            gap: 0.35rem;
            white-space: nowrap;
        }

        .pulse-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background-color: #10b981;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulse-animation 2s infinite;
            display: inline-block;
            flex-shrink: 0;
        }

        @keyframes pulse-animation {
            0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
            100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        .topbar-pill {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 0.2rem 0.55rem;
            border-radius: 0.35rem;
            color: #cbd5e1;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.72rem;
            white-space: nowrap;
        }

        @media (max-width: 768px) {
            .topbar-enterprise {
                flex-direction: column;
                align-items: flex-start;
                padding: 0.5rem 0.75rem;
            }
            .topbar-right {
                display: none; /* Hide secondary timestamps on small mobile to save vertical space */
            }
        }

        /* -------------------------------------------------------------
           2. MAIN CONTAINER & HEADER
           ------------------------------------------------------------- */
        .container {
            width: 100%;
            max-width: 1680px;
            margin: 0 auto;
            padding: 1.25rem 1.25rem 3.5rem 1.25rem;
        }

        @media (max-width: 768px) {
            .container {
                padding: 0.75rem 0.75rem 2.5rem 0.75rem;
            }
        }

        .main-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .main-title h1 {
            font-size: 1.5rem;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.025em;
            line-height: 1.25;
        }

        .main-title p {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }

        @media (max-width: 768px) {
            .main-title h1 { font-size: 1.2rem; }
            .main-title p { font-size: 0.78rem; }
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        @media (max-width: 640px) {
            .header-actions {
                width: 100%;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.4rem;
            }
            .header-actions .btn-matches {
                grid-column: span 2;
            }
        }

        .btn {
            font-family: var(--font-sans);
            font-size: 0.8rem;
            font-weight: 600;
            padding: 0.5rem 0.85rem;
            border-radius: 0.45rem;
            border: 1px solid transparent;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.4rem;
            transition: all 0.15s ease;
            text-decoration: none;
            white-space: nowrap;
        }

        .btn-outline {
            background: #ffffff;
            border-color: var(--border-strong);
            color: #334155;
            box-shadow: var(--shadow-sm);
        }

        .btn-outline:hover {
            background: #f8fafc;
            border-color: #94a3b8;
            color: #0f172a;
        }

        .btn-telegram {
            background: #0284c7;
            color: #ffffff;
            box-shadow: var(--shadow-sm);
        }

        .btn-telegram:hover {
            background: #0369a1;
        }

        .btn-matches {
            background: #ffffff;
            border-color: var(--border-strong);
            color: #1e293b;
            position: relative;
        }

        .btn-matches .badge-count {
            background: #ef4444;
            color: #ffffff;
            font-size: 0.68rem;
            font-weight: 700;
            padding: 0.05rem 0.4rem;
            border-radius: 9999px;
            margin-left: 0.2rem;
        }

        /* -------------------------------------------------------------
           3. COMMAND CENTER: KRİZ TESTİ & CANLI SİMÜLASYON
           ------------------------------------------------------------- */
        .simulation-command-deck {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-radius: 0.75rem;
            padding: 1.1rem 1.35rem;
            margin-bottom: 1.25rem;
            border: 1px solid #334155;
            box-shadow: var(--shadow-md);
            color: #ffffff;
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
        }

        .deck-top-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }

        @media (max-width: 960px) {
            .deck-top-row {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.75rem;
            }
            .deck-actions {
                width: 100%;
                display: flex;
                gap: 0.5rem;
            }
            .deck-actions form {
                flex: 1;
            }
            .deck-actions button {
                width: 100%;
                justify-content: center;
            }
        }

        .deck-info {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        .deck-pill {
            background: rgba(245, 158, 11, 0.18);
            border: 1px solid rgba(245, 158, 11, 0.4);
            color: #fbbf24;
            font-size: 0.68rem;
            font-weight: 700;
            padding: 0.2rem 0.55rem;
            border-radius: 9999px;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            white-space: nowrap;
        }

        .deck-heading {
            font-size: 0.95rem;
            font-weight: 700;
            color: #f8fafc;
            line-height: 1.3;
        }

        .deck-subtitle {
            font-size: 0.775rem;
            color: #94a3b8;
            margin-top: 0.1rem;
            line-height: 1.4;
        }

        .deck-actions {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-shrink: 0;
        }

        .btn-sim-trigger {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: #ffffff;
            font-weight: 700;
            border: none;
            padding: 0.55rem 1rem;
            border-radius: 0.45rem;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.35);
            transition: all 0.2s;
            font-size: 0.8rem;
            white-space: nowrap;
        }

        .btn-sim-trigger:hover {
            transform: translateY(-1px);
            box-shadow: 0 0 18px rgba(245, 158, 11, 0.55);
        }

        .btn-sim-reset {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.16);
            color: #e2e8f0;
            font-weight: 600;
            padding: 0.55rem 0.85rem;
            border-radius: 0.45rem;
            cursor: pointer;
            transition: all 0.15s;
            font-size: 0.8rem;
            white-space: nowrap;
        }

        .btn-sim-reset:hover {
            background: rgba(255, 255, 255, 0.15);
            color: #ffffff;
        }

        /* 3 Adım Uçuş Hattı (Visual Flow) */
        .deck-flight-path {
            display: grid;
            grid-template-columns: 1fr auto 1.3fr auto 1fr;
            align-items: center;
            gap: 0.75rem;
            background: rgba(0, 0, 0, 0.28);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 0.65rem 0.95rem;
            border-radius: 0.5rem;
        }

        @media (max-width: 900px) {
            .deck-flight-path {
                grid-template-columns: 1fr;
                gap: 0.5rem;
            }
            .path-arrow { display: none; }
        }

        .path-step {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            font-size: 0.775rem;
        }

        .step-num {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: 800;
            flex-shrink: 0;
        }

        .step-num.amber { background: #f59e0b; color: #000; }
        .step-num.blue { background: #3b82f6; color: #fff; }
        .step-num.green { background: #10b981; color: #fff; }

        .path-step strong { color: #f8fafc; font-weight: 700; }
        .path-step span { color: #94a3b8; font-size: 0.725rem; }
        .path-arrow { color: #64748b; font-weight: 700; font-size: 0.85rem; }

        /* -------------------------------------------------------------
           4. KPI FINANCIAL CARDS (Proportional & Uniform Height)
           ------------------------------------------------------------- */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 1.25rem;
        }

        @media (max-width: 1024px) {
            .summary-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 580px) {
            .summary-grid { grid-template-columns: 1fr; }
        }

        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 0.65rem;
            padding: 1.1rem 1.2rem;
            box-shadow: var(--shadow-sm);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 125px;
        }

        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: #cbd5e1;
        }

        .kpi-card.kpi-blue::before { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
        .kpi-card.kpi-rose::before { background: linear-gradient(90deg, #f43f5e, #fb7185); }
        .kpi-card.kpi-emerald::before { background: linear-gradient(90deg, #10b981, #34d399); }
        .kpi-card.kpi-indigo::before { background: linear-gradient(90deg, #6366f1, #818cf8); }

        .kpi-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.35rem;
        }

        .kpi-title {
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            white-space: nowrap;
        }

        .kpi-badge {
            font-size: 0.65rem;
            font-weight: 700;
            padding: 0.15rem 0.45rem;
            border-radius: 9999px;
            white-space: nowrap;
        }

        .badge-blue { background: #eff6ff; color: #1d4ed8; }
        .badge-rose { background: #fff1f2; color: #be123c; }
        .badge-emerald { background: #ecfdf5; color: #047857; }
        .badge-indigo { background: #eef2ff; color: #4338ca; }

        .kpi-value {
            font-size: 1.65rem;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.03em;
            display: flex;
            align-items: baseline;
            gap: 0.35rem;
            margin: 0.15rem 0;
            white-space: nowrap;
        }

        .kpi-value small {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
        }

        .kpi-footer {
            font-size: 0.73rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 0.3rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* -------------------------------------------------------------
           5. AI EXECUTIVE BRIEFING TERMINAL (Equal Height Columns)
           ------------------------------------------------------------- */
        .ai-briefing-box {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            margin-bottom: 1.25rem;
            box-shadow: var(--shadow-sm);
            overflow: hidden;
        }

        .ai-header {
            background: linear-gradient(90deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 0.75rem 1.25rem;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .ai-title {
            font-size: 0.85rem;
            font-weight: 800;
            color: #1e293b;
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }

        .ai-body {
            padding: 1rem 1.25rem;
            font-size: 0.825rem;
            line-height: 1.55;
            color: #334155;
        }

        .ai-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-top: 0.75rem;
        }

        @media (max-width: 900px) {
            .ai-grid { grid-template-columns: 1fr; }
        }

        .ai-action-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            padding: 0.8rem 0.95rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .ai-action-card.urgent {
            border-left: 3.5px solid #ef4444;
            background: #fffafa;
        }

        .ai-action-card.profit {
            border-left: 3.5px solid #10b981;
            background: #f0fdf4;
        }

        .ai-card-title {
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }

        .ai-card-title.urgent { color: #b91c1c; }
        .ai-card-title.profit { color: #047857; }

        .ai-chips-list {
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            font-size: 0.75rem;
        }

        .ai-chip-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.35rem 0.55rem;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 0.35rem;
            gap: 0.5rem;
        }

        .ai-chip-row strong {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .ai-chip-row span {
            white-space: nowrap;
            font-size: 0.73rem;
        }

        /* -------------------------------------------------------------
           6. SEARCH & FILTER TOOLBAR (Mobile-Ready)
           ------------------------------------------------------------- */
        .table-toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.85rem;
            flex-wrap: wrap;
            gap: 0.75rem;
        }

        .search-box {
            position: relative;
            flex: 1;
            min-width: 240px;
            max-width: 380px;
        }

        @media (max-width: 640px) {
            .search-box {
                max-width: 100%;
                width: 100%;
            }
        }

        .search-box input {
            width: 100%;
            font-family: var(--font-sans);
            font-size: 0.825rem;
            padding: 0.55rem 0.85rem 0.55rem 2.25rem;
            border: 1px solid var(--border-strong);
            border-radius: 0.45rem;
            background: #ffffff;
            color: var(--text-main);
            outline: none;
            transition: all 0.15s;
        }

        .search-box input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }

        .search-icon {
            position: absolute;
            left: 0.75rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 0.85rem;
            pointer-events: none;
        }

        .filter-tabs {
            display: flex;
            align-items: center;
            gap: 0.25rem;
            background: #e2e8f0;
            padding: 0.2rem;
            border-radius: 0.45rem;
            overflow-x: auto;
            max-width: 100%;
        }

        .tab-btn {
            font-family: var(--font-sans);
            font-size: 0.75rem;
            font-weight: 600;
            border: none;
            background: transparent;
            color: #475569;
            padding: 0.35rem 0.65rem;
            border-radius: 0.35rem;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            transition: all 0.15s;
            white-space: nowrap;
        }

        .tab-btn.active {
            background: #ffffff;
            color: #0f172a;
            box-shadow: var(--shadow-sm);
        }

        .tab-count {
            background: #e2e8f0;
            color: #475569;
            font-size: 0.68rem;
            font-weight: 700;
            padding: 0.05rem 0.35rem;
            border-radius: 9999px;
        }

        .tab-btn.active .tab-count {
            background: #0f172a;
            color: #ffffff;
        }

        /* -------------------------------------------------------------
           7. THE MASTERPIECE TABLE (Responsive with Sticky Product Col)
           ------------------------------------------------------------- */
        .table-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 0.75rem;
            box-shadow: var(--shadow-sm);
            overflow: hidden;
            margin-bottom: 2rem;
            position: relative;
        }

        .table-scroll-hint {
            display: none;
            padding: 0.4rem 0.85rem;
            background: #eff6ff;
            color: #1d4ed8;
            font-size: 0.72rem;
            font-weight: 600;
            text-align: center;
            border-bottom: 1px solid #bfdbfe;
        }

        @media (max-width: 1180px) {
            .table-scroll-hint { display: block; }
        }

        .table-responsive {
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }

        table.catalog-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            text-align: left;
            min-width: 1080px; /* Guarantees no column compression on laptop/mobile */
        }

        table.catalog-table th {
            background: #f8fafc;
            color: #475569;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 0.75rem 0.75rem;
            border-bottom: 1px solid var(--border-subtle);
            white-space: nowrap;
        }

        table.catalog-table td {
            padding: 0.75rem 0.75rem;
            border-bottom: 1px solid var(--border-subtle);
            vertical-align: middle;
            font-size: 0.825rem;
            background: #ffffff;
        }

        table.catalog-table tr:last-child td {
            border-bottom: none;
        }

        table.catalog-table tr.product-row:hover td {
            background-color: #f8fafc;
        }

        /* STICKY COLUMN 1 (Locked on left when scrolling horizontally) */
        @media (max-width: 1180px) {
            table.catalog-table th.col-sticky-1,
            table.catalog-table td.col-sticky-1 {
                position: sticky;
                left: 0;
                z-index: 5;
                background-color: #ffffff;
                box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
            }
            table.catalog-table th.col-sticky-1 {
                background-color: #f8fafc;
                z-index: 6;
            }
        }

        /* Sütun 1: Ürün Hücresi (Device Identity) */
        .cell-product {
            width: 250px;
            min-width: 240px;
        }

        .product-meta-wrap {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .device-avatar {
            width: 40px;
            height: 40px;
            border-radius: 0.45rem;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            border: 1px solid #e2e8f0;
            box-shadow: var(--shadow-sm);
        }

        .product-info-col {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .product-headline {
            font-weight: 700;
            font-size: 0.85rem;
            color: #0f172a;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.35rem;
            line-height: 1.3;
        }

        .product-headline:hover {
            color: var(--primary);
        }

        .brand-chip {
            font-size: 0.62rem;
            font-weight: 800;
            text-transform: uppercase;
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            letter-spacing: 0.04em;
            white-space: nowrap;
        }

        .apple-badge { background: #0f172a; color: #ffffff; }
        .samsung-badge { background: #1e3a8a; color: #ffffff; }
        .xiaomi-badge { background: #ea580c; color: #ffffff; }
        .poco-badge { background: #ca8a04; color: #000000; }

        .product-specs-row {
            display: flex;
            align-items: center;
            gap: 0.25rem;
            flex-wrap: wrap;
        }

        .spec-pill {
            font-size: 0.68rem;
            font-weight: 600;
            background: #f1f5f9;
            color: #475569;
            padding: 0.08rem 0.35rem;
            border-radius: 0.25rem;
            white-space: nowrap;
        }

        .sku-link {
            font-size: 0.7rem;
            color: var(--primary);
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.2rem;
            white-space: nowrap;
        }

        .sku-link:hover { text-decoration: underline; }

        /* Sütun 2: Cep-Hane Fiyatı (Millimeter Height Alignment) */
        .cell-my-price {
            width: 140px;
            min-width: 135px;
        }

        .my-price-card {
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 64px;
            padding: 0.4rem 0.6rem;
            border-radius: 0.45rem;
            border: 1px solid transparent;
        }

        .my-price-card.is-leader {
            background: #f0fdf4;
            border-color: #86efac;
        }

        .leader-crown-tag {
            font-size: 0.65rem;
            font-weight: 800;
            color: #047857;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            height: 16px;
            white-space: nowrap;
        }

        .crown-spacer {
            height: 16px;
            display: block;
        }

        .my-price-val {
            font-family: var(--font-mono);
            font-weight: 800;
            font-size: 0.975rem;
            color: #0f172a;
            white-space: nowrap;
        }

        .my-price-sub {
            font-size: 0.7rem;
            color: #64748b;
            white-space: nowrap;
        }

        /* Sütun 3, 4, 5: Pazaryeri Hücreleri (Equalized 64px Cards) */
        .cell-marketplace {
            width: 155px;
            min-width: 150px;
        }

        .market-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 0.45rem;
            padding: 0.45rem 0.65rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 64px;
            position: relative;
            transition: all 0.15s;
        }

        .market-card.is-winner {
            background: #f0fdf4;
            border: 1.5px solid #10b981;
            box-shadow: 0 0 8px rgba(16, 185, 129, 0.12);
        }

        .market-card.empty-card {
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #94a3b8;
            font-size: 0.73rem;
            font-weight: 600;
        }

        .market-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 16px;
        }

        .market-tag {
            font-size: 0.64rem;
            font-weight: 700;
            padding: 0.08rem 0.35rem;
            border-radius: 0.2rem;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .tag-ptt { background: #002f6c; color: #f9b000; }
        .tag-hb { background: #ff6000; color: #ffffff; }
        .tag-n11 { background: #e62117; color: #ffffff; }

        .market-winner-crown {
            font-size: 0.64rem;
            font-weight: 800;
            color: #059669;
            display: flex;
            align-items: center;
            gap: 0.2rem;
            text-transform: uppercase;
            letter-spacing: 0.02em;
            white-space: nowrap;
        }

        .market-price {
            font-family: var(--font-mono);
            font-weight: 700;
            font-size: 0.925rem;
            color: #0f172a;
            white-space: nowrap;
            margin: 0.1rem 0;
        }

        .market-card.is-winner .market-price {
            color: #047857;
            font-weight: 800;
        }

        .market-store-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.69rem;
            color: #475569;
            white-space: nowrap;
            gap: 0.3rem;
        }

        .market-store-name {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 90px;
        }

        .market-rating {
            color: #ca8a04;
            font-weight: 700;
        }

        .market-stock-chip {
            font-size: 0.67rem;
            font-weight: 600;
            color: #64748b;
            white-space: nowrap;
        }

        .stock-alert { color: #dc2626; font-weight: 700; }

        /* Sütun 6: Fark Çipi */
        .cell-diff {
            width: 130px;
            min-width: 125px;
        }

        .diff-chip-box {
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 64px;
            gap: 0.2rem;
        }

        .diff-pill {
            font-family: var(--font-mono);
            font-weight: 700;
            font-size: 0.8rem;
            padding: 0.2rem 0.5rem;
            border-radius: 0.35rem;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            width: fit-content;
            white-space: nowrap;
        }

        .diff-danger { background: #fee2e2; color: #dc2626; }
        .diff-success { background: #dcfce7; color: #15803d; }
        .diff-gray { background: #f1f5f9; color: #64748b; }

        .diff-winner-name {
            font-size: 0.68rem;
            color: #64748b;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 130px;
        }

        /* Sütun 7: Karar & Aksiyon Kartı (Equalized 64px Card) */
        .cell-action {
            width: 220px;
            min-width: 210px;
        }

        .action-card-widget {
            border-radius: 0.45rem;
            padding: 0.45rem 0.65rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 64px;
        }

        .action-card-widget.buybox {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
        }

        .action-card-widget.profit {
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
        }

        .action-card-widget.risk {
            background: #fff1f2;
            border: 1px solid #fecdd3;
        }

        .action-widget-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 16px;
        }

        .action-widget-badge {
            font-size: 0.65rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            white-space: nowrap;
        }

        .action-card-widget.buybox .action-widget-badge { color: #1d4ed8; }
        .action-card-widget.profit .action-widget-badge { color: #047857; }
        .action-card-widget.risk .action-widget-badge { color: #be123c; }

        .action-widget-price {
            font-family: var(--font-mono);
            font-size: 0.975rem;
            font-weight: 800;
            white-space: nowrap;
            margin: 0.1rem 0;
        }

        .action-card-widget.buybox .action-widget-price { color: #1e3a8a; }
        .action-card-widget.profit .action-widget-price { color: #065f46; }
        .action-card-widget.risk .action-widget-price { color: #9f1239; }

        .action-widget-sub {
            font-size: 0.68rem;
            color: #475569;
            display: flex;
            align-items: center;
            gap: 0.3rem;
            white-space: nowrap;
        }

        .action-tag {
            background: rgba(255, 255, 255, 0.7);
            padding: 0.05rem 0.3rem;
            border-radius: 0.2rem;
            font-weight: 600;
            white-space: nowrap;
        }

        /* -------------------------------------------------------------
           8. SEKTÖREL MODÜLLER (Tam Sürüm Yol Haritası)
           ------------------------------------------------------------- */
        .roadmap-section {
            background: #0f172a;
            border-radius: 0.75rem;
            padding: 1.75rem 1.75rem;
            color: #ffffff;
            margin-top: 2rem;
            border: 1px solid #1e293b;
        }

        .roadmap-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .roadmap-header h2 {
            font-size: 1.25rem;
            font-weight: 800;
            color: #f8fafc;
        }

        .roadmap-header p {
            font-size: 0.8rem;
            color: #94a3b8;
            margin-top: 0.2rem;
            max-width: 900px;
        }

        .roadmap-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
        }

        @media (max-width: 1200px) {
            .roadmap-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 640px) {
            .roadmap-grid { grid-template-columns: 1fr; }
        }

        .roadmap-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 0.55rem;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            transition: all 0.2s;
        }

        .roadmap-card:hover {
            border-color: #3b82f6;
            transform: translateY(-2px);
        }

        .roadmap-card-tag {
            font-size: 0.62rem;
            font-weight: 700;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .roadmap-card h3 {
            font-size: 0.875rem;
            font-weight: 700;
            color: #f8fafc;
        }

        .roadmap-card p {
            font-size: 0.75rem;
            color: #94a3b8;
            line-height: 1.45;
        }

        /* -------------------------------------------------------------
           9. CANLI AKSİYON MODALI (Progress Modal)
           ------------------------------------------------------------- */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(6px);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal-card {
            background: #ffffff;
            border-radius: 1rem;
            width: 100%;
            max-width: 520px;
            padding: 1.75rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
            text-align: center;
        }

        .modal-spinner-ring {
            width: 48px;
            height: 48px;
            border: 4px solid #e2e8f0;
            border-top: 4px solid #f59e0b;
            border-radius: 50%;
            animation: spin 0.9s linear infinite;
            margin: 0 auto 1rem auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .modal-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.25rem;
        }

        .modal-desc {
            font-size: 0.8rem;
            color: #64748b;
            margin-bottom: 1.25rem;
        }

        .progress-bar-track {
            height: 8px;
            background: #e2e8f0;
            border-radius: 9999px;
            overflow: hidden;
            margin-bottom: 1.25rem;
        }

        .progress-bar-fill {
            height: 100%;
            width: 15%;
            background: linear-gradient(90deg, #f59e0b, #ef4444);
            border-radius: 9999px;
            transition: width 0.3s ease;
        }

        .modal-steps-list {
            text-align: left;
            display: flex;
            flex-direction: column;
            gap: 0.55rem;
            font-size: 0.78rem;
            color: #475569;
        }

        .modal-step-item {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            opacity: 0.4;
            transition: all 0.25s;
        }

        .modal-step-item.active {
            opacity: 1;
            font-weight: 700;
            color: #0f172a;
        }

        .modal-step-item.done {
            opacity: 0.9;
            color: #059669;
        }

        .step-icon {
            font-size: 0.9rem;
        }
    </style>
</head>
<body>

    <!-- 1. KURUMSAL TOPBAR -->
    <header class="topbar-enterprise">
        <div class="topbar-left">
            <span class="topbar-badge">ÖZEL DEMO ORTAMI</span>
            <span class="topbar-company">
                <strong>Cep-Hane Teknoloji</strong> (cephaneteknoloji.com) — Mersin
            </span>
            <span class="topbar-pill">
                <span class="pulse-dot"></span>
                Canlı Pazaryeri Motoru Aktif
            </span>
            <span class="topbar-pill">
                📦 Katalog: 210 Ürün (12 Model)
            </span>
        </div>
        <div class="topbar-right">
            <span class="topbar-pill">
                🤖 Telegram: @Cep-haneFiyatTakipBot
            </span>
            <span class="topbar-pill">
                🕒 Son Tarama: 2026-10-31 12:11:38
            </span>
        </div>
    </header>

    <div class="container">

        <!-- 2. ANA SAYFA BAŞLIĞI VE AKSİYONLAR -->
        <div class="main-header">
            <div class="main-title">
                <h1>Fiyat Takip, Satıcı Analizi & Rekabet Karar Destek Merkezi</h1>
                <p>cephaneteknoloji.com ürün kataloğunun PttAVM, Hepsiburada ve N11/Pazarama mağazalarıyla anlık rekabet ve kâr analizi</p>
            </div>
            <div class="header-actions">
                <a href="/indir/onerilen-fiyatlar.xlsx" class="btn btn-outline" title="Tüm fiyat önerilerini Excel olarak indir">
                    📊 .xlsx Fiyat Raporu İndir
                </a>
                <form method="post" action="/demo/telegram-gonder" style="display:inline;">
                    <button type="submit" class="btn btn-telegram" title="Cep-Hane Telegram kanalına anlık brifing atar">
                        📲 Telegram'a Brifing Gönder
                    </button>
                </form>
                <a href="/eslesmeler" class="btn btn-matches">
                    Eşleşme Onayı
                    {% if ozet.onay_bekleyen_eslesme_sayisi > 0 %}
                        <span class="badge-count">{{ ozet.onay_bekleyen_eslesme_sayisi }} Bekleyen</span>
                    {% else %}
                        <span style="color:var(--text-muted);font-weight:400;">(0)</span>
                    {% endif %}
                </a>
            </div>
        </div>

        <!-- 3. CANLI SİMÜLASYON & KRİZ TESTİ KUMANDA MASASI -->
        <section class="simulation-command-deck">
            <div class="deck-top-row">
                <div class="deck-info">
                    <span class="deck-pill">
                        ⚡ CANLI TEST MASASI
                    </span>
                    <div>
                        <div class="deck-heading">Pazaryeri Ani Fiyat Kırma Testi: Apple iPhone 15 128 GB Siyah</div>
                        <div class="deck-subtitle">Rakip (N11 / TeknoMerkez) fiyatını aniden 58.750 TL'den 57.490 TL'ye (-1.260 TL) indirdiğinde sistemin marjınızı nasıl savunduğunu görün.</div>
                    </div>
                </div>
                <div class="deck-actions">
                    <form method="post" action="/demo/fiyat-dusur" id="simForm" style="display:inline;">
                        <button type="submit" class="btn-sim-trigger" id="btnSimulate">
                            ⚡ Rakip İndirimi Simüle Et (-1.260 TL)
                        </button>
                    </form>
                    <form method="post" action="/demo/sifirla" style="display:inline;">
                        <button type="submit" class="btn-sim-reset" title="Demoyu başlangıç ayarlarına döndür">
                            🔄 Demoyu Sıfırla
                        </button>
                    </form>
                </div>
            </div>

            <div class="deck-flight-path">
                <div class="path-step">
                    <div class="step-num amber">1</div>
                    <div>
                        <strong>1. Kriz Senaryosu:</strong> <span>Rakip anında 57.490 TL'ye iner</span>
                    </div>
                </div>
                <div class="path-arrow">➔</div>
                <div class="path-step">
                    <div class="step-num blue">2</div>
                    <div>
                        <strong>2. Akıllı Havale Dip Koruması:</strong> <span>58.000 TL dip sınır altına inilmez</span>
                    </div>
                </div>
                <div class="path-arrow">➔</div>
                <div class="path-step">
                    <div class="step-num green">3</div>
                    <div>
                        <strong>3. Anlık Kriz Alarmı:</strong> <span>Telegram @Cep-haneFiyatTakipBot'a acil uyarı gider</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- 4. FİNANSAL VE OPERASYONEL KPI KARTLARI -->
        <section class="summary-grid">
            <div class="kpi-card kpi-blue">
                <div class="kpi-header">
                    <span class="kpi-title">Katalog Kapsamı</span>
                    <span class="kpi-badge badge-blue">Katalog Tespiti</span>
                </div>
                <div class="kpi-value">
                    {{ ozet.toplam_urun }} <small>/ 210 Model</small>
                </div>
                <div class="kpi-footer">
                    <span>cephaneteknoloji.com'da 210 ürün</span>
                </div>
            </div>

            <div class="kpi-card kpi-rose">
                <div class="kpi-header">
                    <span class="kpi-title">Rakip Avantajı</span>
                    <span class="kpi-badge badge-rose">Rakip Ucuz</span>
                </div>
                <div class="kpi-value" style="color:var(--rose);">
                    {{ ozet.rakibin_ucuz_oldugu_urun_sayisi }} <small>Ürün</small>
                </div>
                <div class="kpi-footer">
                    <span><strong>{{ dip_alti_sayisi }}</strong> üründe dip sınır koruması devrede</span>
                </div>
            </div>

            <div class="kpi-card kpi-emerald">
                <div class="kpi-header">
                    <span class="kpi-title">Net Kâr Potansiyeli</span>
                    <span class="kpi-badge badge-emerald">Ekstra Marj</span>
                </div>
                <div class="kpi-value" style="color:var(--emerald);">
                    +{{ toplam_birim_ek_kar|tr_fiyat }} <small>TL / adet</small>
                </div>
                <div class="kpi-footer" style="color:var(--emerald);font-weight:600;">
                    <span>👑 10'ar satışta <strong>+{{ toplam_10lu_ek_kar|tr_fiyat }} TL</strong> ek kâr</span>
                </div>
            </div>

            <div class="kpi-card kpi-indigo">
                <div class="kpi-header">
                    <span class="kpi-title">Pazaryeri Motoru</span>
                    <span class="kpi-badge badge-indigo">Canlı Veri</span>
                </div>
                <div class="kpi-value">
                    3 <small>Pazaryeri</small>
                </div>
                <div class="kpi-footer">
                    <span>PttAVM · Hepsiburada · N11/Pazarama</span>
                </div>
            </div>
        </section>

        <!-- 5. YAPAY ZEKA SATIN ALMA & STRATEJİ DİREKTİFİ -->
        <section class="ai-briefing-box">
            <div class="ai-header">
                <div class="ai-title">
                    <span>🧠</span>
                    Yapay Zeka Satın Alma & Fiyat Stratejisi Direktifi
                </div>
                <span class="topbar-pill" style="color:#0f172a;background:#e2e8f0;border:none;font-weight:600;">
                    🤖 @Cep-haneFiyatTakipBot ile Canlı Senkronize
                </span>
            </div>
            <div class="ai-body">
                <p>
                    <strong>Günün Özeti:</strong> İzlenen 12 amiral ürünün <strong>9 tanesinde</strong> pazaryeri rakiplerimiz (PttAVM, Hepsiburada, N11) liste fiyatımızın altında satış yapmaktadır. Ancak <strong>'Samsung Galaxy A17'</strong> gibi ürünlerde rakipler dip sınırımızın yakınına indiği için gereksiz fiyat kırmayarak kârlılığımız başarıyla korunmuştur.
                </p>
                <div class="ai-grid">
                    <div class="ai-action-card urgent">
                        <div class="ai-card-title urgent">
                            <span>🎯</span>
                            Acil Fiyatlandırma Aksiyonları (1. Sırayı Al)
                        </div>
                        <div class="ai-chips-list">
                            <div class="ai-chip-row">
                                <strong>Apple iPhone 15 128 GB</strong>
                                <span>Önerilen: <strong>58.650,00 TL</strong></span>
                            </div>
                            <div class="ai-chip-row">
                                <strong>POCO X8 Pro 256 GB</strong>
                                <span>Önerilen: <strong>33.850,00 TL</strong></span>
                            </div>
                            <div class="ai-chip-row">
                                <strong>Samsung Galaxy A36 5G</strong>
                                <span>Önerilen: <strong>24.850,00 TL</strong></span>
                            </div>
                        </div>
                    </div>

                    <div class="ai-action-card profit">
                        <div class="ai-card-title profit">
                            <span>👑</span>
                            Marj Artırma Fırsatları (Fiyatı Güvenle Yukarı Çek)
                        </div>
                        <div class="ai-chips-list">
                            <div class="ai-chip-row">
                                <strong>Samsung Galaxy A26 256 GB</strong>
                                <span style="color:#047857;"><strong>23.290,00 TL</strong> (+390 TL Kâr)</span>
                            </div>
                            <div class="ai-chip-row">
                                <strong>Apple iPad Mini 7 512 GB</strong>
                                <span style="color:#047857;"><strong>59.000,00 TL</strong> (+700 TL Kâr)</span>
                            </div>
                            <div class="ai-chip-row">
                                <strong>Xiaomi Redmi Pad 2</strong>
                                <span style="color:#047857;"><strong>7.240,00 TL</strong> (+140 TL Kâr)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 6. FİLTRELER VE ARAMA ÇUBUĞU -->
        <div class="table-toolbar">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" placeholder="Model adı, satıcı mağaza veya SKU ara...">
            </div>
            <div class="filter-tabs">
                <button type="button" class="tab-btn active" data-filter="all">
                    Tümü <span class="tab-count">{{ urunler|length }}</span>
                </button>
                <button type="button" class="tab-btn" data-filter="cheaper">
                    🔴 Rakip Ucuz <span class="tab-count">{{ ozet.rakibin_ucuz_oldugu_urun_sayisi }}</span>
                </button>
                <button type="button" class="tab-btn" data-filter="dip">
                    ⚠️ Dip Sınır Riski <span class="tab-count">{{ dip_alti_sayisi }}</span>
                </button>
                <button type="button" class="tab-btn" data-filter="opportunity">
                    👑 Kâr Fırsatı <span class="tab-count">{{ firsat_sayisi }}</span>
                </button>
            </div>
        </div>

        <!-- 7. ANA REKABET VE FİYATLANDIRMA TABLOSU (Responsive & Locked Sticky Column) -->
        <div class="table-card">
            <div class="table-scroll-hint">
                👉 Tabloyu sağa/sola kaydırarak tüm pazaryeri satıcılarını ve önerileri inceleyebilirsiniz
            </div>
            <div class="table-responsive">
                <table class="catalog-table" id="productsTable">
                    <thead>
                        <tr>
                            <th class="col-sticky-1">Ürün &amp; Cihaz Kimliği</th>
                            <th>Cep-Hane Fiyatı</th>
                            <th>PttAVM Satıcı Kartı</th>
                            <th>Hepsiburada Satıcı Kartı</th>
                            <th>N11 / Pazarama Satıcı Kartı</th>
                            <th>En Ucuz Rakip &amp; Fark</th>
                            <th>Akıllı Karar &amp; Fiyat Önerisi</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for u in urunler %}
                        {% set is_cheaper = (u.durum == "RAKİP UCUZ") %}
                        {% set is_expensive = (u.durum == "BİZ UCUZUZ") %}
                        {% set is_dip = u.dip_alti %}
                        <tr
                            class="product-row"
                            data-name="{{ u.urun_adi|lower }} {{ u.sku|lower }} {{ u.rakip_a_detay.satici|lower if u.rakip_a_detay else '' }} {{ u.rakip_b_detay.satici|lower if u.rakip_b_detay else '' }} {{ u.rakip_c_detay.satici|lower if u.rakip_c_detay else '' }}"
                            data-cheaper="{{ 'true' if is_cheaper else 'false' }}"
                            data-dip="{{ 'true' if is_dip else 'false' }}"
                            data-opportunity="{{ 'true' if is_expensive else 'false' }}"
                        >
                            <!-- 1. Ürün & Cihaz Kimliği (Sticky Locked on Left) -->
                            <td class="cell-product col-sticky-1">
                                <div class="product-meta-wrap">
                                    <div class="device-avatar" style="background:{{ u.visual.bg_color }};">
                                        {{ u.visual.svg_icon|safe }}
                                    </div>
                                    <div class="product-info-col">
                                        <div class="product-specs-row">
                                            <span class="brand-chip {{ u.visual.brand_badge }}">{{ u.visual.brand }}</span>
                                            {% for spec in u.visual.specs %}
                                                <span class="spec-pill">{{ spec }}</span>
                                            {% endfor %}
                                        </div>
                                        <a href="/urun/{{ u.id }}" class="product-headline" title="{{ u.urun_adi }}">
                                            {{ u.visual.short_title }}
                                        </a>
                                        <a href="/urun/{{ u.id }}" class="sku-link">
                                            {{ u.sku }} · Grafik &amp; Analiz →
                                        </a>
                                    </div>
                                </div>
                            </td>

                            <!-- 2. Cep-Hane Fiyatı (Millimeter-Aligned) -->
                            <td class="cell-my-price">
                                <div class="my-price-card {% if u.cep_hane_is_leader %}is-leader{% endif %}">
                                    {% if u.cep_hane_is_leader %}
                                        <div class="leader-crown-tag">👑 1. SIRA BİZDE</div>
                                    {% else %}
                                        <div class="crown-spacer"></div>
                                    {% endif %}
                                    <div class="my-price-val">{{ u.benim_fiyatim|tr_fiyat }} TL</div>
                                    <div class="my-price-sub">Havale Dip: {{ u.min_kabul_edilebilir_fiyat|tr_fiyat }} TL</div>
                                </div>
                            </td>

                            <!-- 3. PttAVM (Equal 64px Height Card) -->
                            <td class="cell-marketplace">
                                {% if u.rakip_a_detay %}
                                    <div class="market-card {% if u.rakip_a_detay.is_cheapest %}is-winner{% endif %}">
                                        <div class="market-header">
                                            <span class="market-tag tag-ptt">PttAVM</span>
                                            {% if u.rakip_a_detay.is_cheapest %}
                                                <span class="market-winner-crown">🏆 EN UCUZ</span>
                                            {% endif %}
                                        </div>
                                        <div class="market-price">{{ u.rakip_a_detay.fiyat|tr_fiyat }} TL</div>
                                        <div class="market-store-row">
                                            <span class="market-store-name" title="{{ u.rakip_a_detay.satici }}">🏪 {{ u.rakip_a_detay.satici }}</span>
                                            <span class="market-rating">★ {{ u.rakip_a_detay.puan }}</span>
                                        </div>
                                    </div>
                                {% else %}
                                    <div class="market-card empty-card">
                                        <a href="/eslesmeler" style="color:#b45309;text-decoration:underline;">⏳ Eşleşme Bekliyor</a>
                                    </div>
                                {% endif %}
                            </td>

                            <!-- 4. Hepsiburada (Equal 64px Height Card) -->
                            <td class="cell-marketplace">
                                {% if u.rakip_b_detay %}
                                    <div class="market-card {% if u.rakip_b_detay.is_cheapest %}is-winner{% endif %}">
                                        <div class="market-header">
                                            <span class="market-tag tag-hb">Hepsiburada</span>
                                            {% if u.rakip_b_detay.is_cheapest %}
                                                <span class="market-winner-crown">🏆 EN UCUZ</span>
                                            {% endif %}
                                        </div>
                                        <div class="market-price">{{ u.rakip_b_detay.fiyat|tr_fiyat }} TL</div>
                                        <div class="market-store-row">
                                            <span class="market-store-name" title="{{ u.rakip_b_detay.satici }}">🏪 {{ u.rakip_b_detay.satici }}</span>
                                            <span class="market-rating">★ {{ u.rakip_b_detay.puan }}</span>
                                        </div>
                                    </div>
                                {% else %}
                                    <div class="market-card empty-card">
                                        <span>- İlan Yok -</span>
                                    </div>
                                {% endif %}
                            </td>

                            <!-- 5. N11 / Pazarama (Equal 64px Height Card) -->
                            <td class="cell-marketplace">
                                {% if u.rakip_c_detay %}
                                    <div class="market-card {% if u.rakip_c_detay.is_cheapest %}is-winner{% endif %}">
                                        <div class="market-header">
                                            <span class="market-tag tag-n11">N11 / Pazarama</span>
                                            {% if u.rakip_c_detay.is_cheapest %}
                                                <span class="market-winner-crown">🏆 EN UCUZ</span>
                                            {% endif %}
                                        </div>
                                        <div class="market-price">{{ u.rakip_c_detay.fiyat|tr_fiyat }} TL</div>
                                        <div class="market-store-row">
                                            <span class="market-store-name" title="{{ u.rakip_c_detay.satici }}">🏪 {{ u.rakip_c_detay.satici }}</span>
                                            <span class="market-rating">★ {{ u.rakip_c_detay.puan }}</span>
                                        </div>
                                    </div>
                                {% else %}
                                    <div class="market-card empty-card">
                                        <span>- İlan Yok -</span>
                                    </div>
                                {% endif %}
                            </td>

                            <!-- 6. En Ucuz Rakip & Fark (Equal 64px Height Card) -->
                            <td class="cell-diff">
                                <div class="diff-chip-box">
                                    {% if u.fark is not none %}
                                        <div class="diff-pill {% if is_cheaper %}diff-danger{% elif is_expensive %}diff-success{% else %}diff-gray{% endif %}">
                                            {{ u.fark|tr_fark }} TL ({{ "%+.1f"|format(u.fark_yuzde) }}%)
                                        </div>
                                        {% if u.en_ucuz_rakip_detay %}
                                            <div class="diff-winner-name" title="{{ u.en_ucuz_rakip_detay.kanal }} / {{ u.en_ucuz_rakip_detay.satici }}">
                                                En Ucuz: <strong>{{ u.en_ucuz_rakip_detay.kanal }}</strong>
                                            </div>
                                        {% endif %}
                                    {% else %}
                                        <span style="color:#94a3b8;">-</span>
                                    {% endif %}
                                </div>
                            </td>

                            <!-- 7. Akıllı Karar & Fiyat Önerisi (Equal 64px Height Card) -->
                            <td class="cell-action">
                                {% if is_dip %}
                                    <div class="action-card-widget risk">
                                        <div class="action-widget-header">
                                            <span class="action-widget-badge">⚠️ DİP SINIR KORUMASI</span>
                                            <span class="action-tag" style="color:#be123c;">Fiyat Kırılmaz</span>
                                        </div>
                                        <div class="action-widget-price">{{ u.min_kabul_edilebilir_fiyat|tr_fiyat }} TL</div>
                                        <div class="action-widget-sub">
                                            <span>Mevcut marj korunur</span>
                                        </div>
                                    </div>
                                {% elif is_cheaper %}
                                    <div class="action-card-widget buybox">
                                        <div class="action-widget-header">
                                            <span class="action-widget-badge">🎯 1. SIRAYI AL</span>
                                            <span class="action-tag">Rakip Altı</span>
                                        </div>
                                        <div class="action-widget-price">{{ u.onerilen_fiyat|tr_fiyat }} TL</div>
                                        <div class="action-widget-sub">
                                            <span class="action-tag">🛡️ %{{ u.yeni_marj_yuzde }} Marj</span>
                                            <span>Havale dip korunur</span>
                                        </div>
                                    </div>
                                {% elif is_expensive %}
                                    <div class="action-card-widget profit">
                                        <div class="action-widget-header">
                                            <span class="action-widget-badge">👑 MARJ FIRSATI</span>
                                            <span class="action-tag" style="color:#047857;">Lider Biziz</span>
                                        </div>
                                        <div class="action-widget-price">{{ u.onerilen_fiyat|tr_fiyat }} TL</div>
                                        <div class="action-widget-sub">
                                            <span class="action-tag">+{{ ((u.onerilen_fiyat or 0) - u.benim_fiyatim)|tr_fiyat }} TL/Adet</span>
                                            <span>1. Sıra Korunur</span>
                                        </div>
                                    </div>
                                {% else %}
                                    <div class="action-card-widget" style="background:#f8fafc;border:1px solid #e2e8f0;">
                                        <div class="action-widget-header">
                                            <span class="action-widget-badge" style="color:#64748b;">FİYAT EŞİT</span>
                                        </div>
                                        <div class="action-widget-price" style="color:#0f172a;">{{ u.benim_fiyatim|tr_fiyat }} TL</div>
                                        <div class="action-widget-sub">
                                            <span>Mevcut fiyat korunur</span>
                                        </div>
                                    </div>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                <div id="emptyState" style="display:none;padding:2rem;text-align:center;color:#64748b;font-weight:600;">
                    Arama kriterlerine uygun ürün bulunamadı.
                </div>
            </div>
        </div>

        <!-- 8. TAM SÜRÜM ELEKTRONİK MODÜLLERİ (Yol Haritası) -->
        <section class="roadmap-section">
            <div class="roadmap-header">
                <div>
                    <h2>🚀 Cep-Hane Teknoloji — Tam Sürüm Sektörel Modülleri &amp; Terzi İşi Avantajlarımız</h2>
                    <p>Bu ekran, sistemin çalışma mantığını hemen test edebilmeniz için <strong>cephaneteknoloji.com</strong> kataloğunuzdaki 12 popüler modelle hazırlanmış canlı demo ortamıdır. Tam sürüm kurulumunda elektronik ve cep telefonu sektörüne özel olarak devreye girecek 8 modül:</p>
                </div>
                <span class="topbar-pill" style="background:#1e3a8a;color:#93c5fd;border:none;font-weight:700;">
                    8 Sektörel Modül · Canlı Kurulum
                </span>
            </div>
            <div class="roadmap-grid">
                <div class="roadmap-card">
                    <span class="roadmap-card-tag">Risk &amp; Marj Koruma</span>
                    <h3>🛡️ 1. Ölü Fiyat &amp; 1 Stok Filtresi</h3>
                    <p>Elinde sadece 1 adet stok kalan, teşhir ürünü satan veya mağaza puanı <strong>9.2'nin altında</strong> olan satıcıların piyasayı bozan yanıltıcı fiyatlarını otomatik filtreler; gereksiz yere fiyat kırmanızı önler.</p>
                </div>
                <div class="roadmap-card">
                    <span class="roadmap-card-tag">Satın Alma İstihbaratı</span>
                    <h3>📦 2. "Toptan Alım Fırsatı" Radarı</h3>
                    <p>Pazaryerinde bir satıcı nakit sıkışıklığı nedeniyle sizin toptan alış maliyetinizin bile altında fiyat açarsa, fiyat kırmak yerine "Bu satıcıdan toptan mal çekme fırsatı" olarak Satın Alma Müdürlüğü'ne alarm verir.</p>
                </div>
                <div class="roadmap-card">
                    <span class="roadmap-card-tag">Finans &amp; Kâr Hesabı</span>
                    <h3>📊 3. Komisyon &amp; Kargo Net Marj Motoru</h3>
                    <p>PttAVM, Hepsiburada, N11 ve Trendyol'un kategori komisyon oranları ile kargo baremlerini ayrı ayrı düşerek brüt satış fiyatı değil, Cep-Hane'ye kalan <strong>net tutar ve Havale dip sınırını</strong> önerir.</p>
                </div>
                <div class="roadmap-card">
                    <span class="roadmap-card-tag">Elektronik Eşleştirme</span>
                    <h3>🔍 4. Renk, GB ve Garanti Ayrıştırıcı</h3>
                    <p>Cep telefonlarında Siyah/Mavi renk fiyat farklarını, 128GB / 256GB kapasiteleri ve <strong>Türkiye Garantili vs. İthalatçı Garantili</strong> ayrımlarını yapay zeka ile denetleyerek elma ile elmayı karşılaştırır.</p>
                </div>
                <div class="roadmap-card">
                    <span class="roadmap-card-tag">Katalog Kapsamı</span>
                    <h3>🌐 5. 210 Ürünün Tamamı &amp; 9 Pazaryeri</h3>
                    <p>Sitenizdeki 7 kategoride yer alan <strong>210 ürünün tamamını</strong> (veya özel Excel/ERP listenizi) Akakçe, Cimri, PttAVM, Hepsiburada, N11, Pazarama, Trendyol, Amazon ve MediaMarkt'ta otomatik tarar.</p>
                </div>
                <div class="roadmap-card">
                    <span class="roadmap-card-tag">ERP / Entegratör</span>
                    <h3>🔄 6. PraPazar &amp; ERP Toplu Fiyat Güncelleme</h3>
                    <p>Sistemin önerdiği ve onayladığınız rekabetçi fiyatları tek tıkla <strong>PraPazar toplu fiyat güncelleme</strong> şablonuna uygun Excel olarak indirir veya doğrudan entegrasyonla pazaryerlerine aktarır.</p>
                </div>
                <div class="roadmap-card">
                    <span class="roadmap-card-tag">Kritik Alarm</span>
                    <h3>⚡ 7. Saatlik "Buybox &amp; Stok" Anlık Alarmı</h3>
                    <p>Sabah 08:30 brifingine ek olarak, en çok ciro getiren "A Grubu" telefon modellerinde gün içinde bir rakip fiyat kırdığında veya stoğu tükendiğinde dakikasında Telegram'dan anlık bildirim gönderir.</p>
                </div>
                <div class="roadmap-card">
                    <span class="roadmap-card-tag">Stratejik İstihbarat</span>
                    <h3>📈 8. Rakip Mağaza Davranış &amp; Trend Analizi</h3>
                    <p>"Bittibitti, GpnTeknoloji veya TeknoMerkez hangi gün ve saatlerde fiyat kırıyor? Hangi markada kim daha agresif?" sorularını yanıtlayan haftalık yönetici strateji raporu üretir.</p>
                </div>
            </div>
        </section>

    </div>

    <!-- 9. CANLI AKSİYON MODALI (Progress Modal) -->
    <div id="progressModal" class="modal-overlay">
        <div class="modal-card">
            <div class="modal-spinner-ring"></div>
            <div class="modal-title" id="modalTitle">Pazaryeri Fiyat Kırma Simülasyonu Başlatıldı</div>
            <div class="modal-desc" id="modalDesc">Apple iPhone 15 128 GB için anlık fiyat taraması ve Havale Dip Sınırı denetimi yapılıyor...</div>
            <div class="progress-bar-track">
                <div class="progress-bar-fill" id="progressFill"></div>
            </div>
            <div class="modal-steps-list">
                <div class="modal-step-item" id="mStep1">
                    <span class="step-icon">📡</span>
                    <span>1. Adım: N11 / TeknoMerkez güncel kampanya fiyatı çekiliyor (57.490 TL)</span>
                </div>
                <div class="modal-step-item" id="mStep2">
                    <span class="step-icon">🛡️</span>
                    <span>2. Adım: Havale Dip Sınırı &amp; Marj Kural Motoru denetleniyor (Dip Sınır: 58.000 TL)</span>
                </div>
                <div class="modal-step-item" id="mStep3">
                    <span class="step-icon">🧠</span>
                    <span>3. Adım: Yapay Zeka Satın Alma &amp; Fiyatlandırma Tavsiyesi güncelleniyor</span>
                </div>
                <div class="modal-step-item" id="mStep4">
                    <span class="step-icon">📲</span>
                    <span>4. Adım: Telegram Yönetici Alarmı (@Cep-haneFiyatTakipBot) iletiliyor</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Tab Arama ve Filtreleme
        const searchInput = document.getElementById('searchInput');
        const tabBtns = document.querySelectorAll('.tab-btn');
        const rows = document.querySelectorAll('.product-row');
        const emptyState = document.getElementById('emptyState');

        let currentFilter = 'all';

        function filterProducts() {
            const query = (searchInput.value || '').toLowerCase().trim();
            let visibleCount = 0;

            rows.forEach(row => {
                const rowText = row.getAttribute('data-name') || '';
                const isCheaper = row.getAttribute('data-cheaper') === 'true';
                const isDip = row.getAttribute('data-dip') === 'true';
                const isOpportunity = row.getAttribute('data-opportunity') === 'true';

                let matchesFilter = true;
                if (currentFilter === 'cheaper') matchesFilter = isCheaper;
                else if (currentFilter === 'dip') matchesFilter = isDip;
                else if (currentFilter === 'opportunity') matchesFilter = isOpportunity;

                let matchesSearch = true;
                if (query.length > 0) {
                    matchesSearch = rowText.includes(query);
                }

                if (matchesFilter && matchesSearch) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            if (emptyState) {
                emptyState.style.display = (visibleCount === 0) ? 'block' : 'none';
            }
        }

        if (searchInput) {
            searchInput.addEventListener('input', filterProducts);
        }

        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.getAttribute('data-filter') || 'all';
                filterProducts();
            });
        });

        // Simülasyon Modal & Progress Tetikleyici
        const simForm = document.getElementById('simForm');
        const progressModal = document.getElementById('progressModal');
        const progressFill = document.getElementById('progressFill');
        const mStep1 = document.getElementById('mStep1');
        const mStep2 = document.getElementById('mStep2');
        const mStep3 = document.getElementById('mStep3');
        const mStep4 = document.getElementById('mStep4');

        if (simForm && progressModal) {
            simForm.addEventListener('submit', function(e) {
                e.preventDefault();
                progressModal.classList.add('active');

                // Adım 1
                progressFill.style.width = '25%';
                mStep1.classList.add('active');

                setTimeout(() => {
                    mStep1.classList.remove('active');
                    mStep1.classList.add('done');
                    mStep2.classList.add('active');
                    progressFill.style.width = '55%';
                }, 600);

                setTimeout(() => {
                    mStep2.classList.remove('active');
                    mStep2.classList.add('done');
                    mStep3.classList.add('active');
                    progressFill.style.width = '80%';
                }, 1200);

                setTimeout(() => {
                    mStep3.classList.remove('active');
                    mStep3.classList.add('done');
                    mStep4.classList.add('active');
                    progressFill.style.width = '100%';
                }, 1800);

                setTimeout(() => {
                    simForm.submit();
                }, 2400);
            });
        }
    </script>
</body>
</html>
"""

tmpl_path.write_text(new_html, encoding="utf-8")
print("Saved millimeter-perfect responsive template to index.html!")

