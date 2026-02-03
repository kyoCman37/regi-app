from django.shortcuts import render, redirect
from django.conf import settings

# ----------------------
# 共通
# ----------------------

def to_int(value):
    if value == "" or value is None:
        return 0
    return int(value)

# ログインチェック（True / False を返す）
def auth_check(request):
    return request.session.get("auth", False)


# ----------------------
# START（ログイン）
# ----------------------

def start(request):
    if request.method == "POST":
        if request.POST.get("code") == settings.LOGIN_CODE:
            request.session["auth"] = True
            return redirect("/regi1/")
    return render(request, "register/start.html")


# ----------------------
# レジ1
# ----------------------

def regi1_input(request):
    if not auth_check(request):
        return redirect("/")
    return render(request, "register/regi1_input.html",
                  request.session.get("regi1_detail", {}))


def regi1_result(request):
    if not auth_check(request):
        return redirect("/")

    # 金種テーブル（1箇所で管理）
    bills_coins = [
        ("10000円", "yen10000", 10000),
        ("5000円",  "yen5000",   5000),
        ("1000円",  "yen1000",   1000),
        ("500円",   "yen500",     500),
        ("100円",   "yen100",     100),
        ("50円",    "yen50",       50),
        ("10円",    "yen10",       10),
        ("5円",     "yen5",         5),
        ("1円",     "yen1",         1),
    ]

    # 入力値（枚数）を安全にint化して集める
    detail = {}
    for _, key, _ in bills_coins:
        detail[key] = to_int(request.POST.get(key))

    # 金種別の金額（例：500円×3枚=1500円）を作る
    denoms = []
    for label, key, unit in bills_coins:
        count = detail[key]
        amount = unit * count
        denoms.append({
            "label": label,
            "count": count,
            "unit": unit,
            "amount": amount,
        })

    total = sum(d["amount"] for d in denoms)

    # セッション保存（保持用）
    request.session["regi1_total"] = total
    request.session["regi1_detail"] = detail
    request.session["regi1_denoms"] = denoms  # ←（任意）あとで一覧表示に使える

    return render(request, "register/regi1_result.html", {
        "total": total,
        "denoms": denoms,  # ← テンプレで一覧表示できる
    })



# ----------------------
# レジ2
# ----------------------

def regi2_input(request):
    if not auth_check(request):
        return redirect("/")
    return render(request, "register/regi2_input.html",
                  request.session.get("regi2_detail", {}))


def regi2_result(request):
    if not auth_check(request):
        return redirect("/")

    # 金種テーブル（1箇所で管理）
    bills_coins = [
        ("10000円", "yen10000", 10000),
        ("5000円",  "yen5000",   5000),
        ("1000円",  "yen1000",   1000),
        ("500円",   "yen500",     500),
        ("100円",   "yen100",     100),
        ("50円",    "yen50",       50),
        ("10円",    "yen10",       10),
        ("5円",     "yen5",         5),
        ("1円",     "yen1",         1),
    ]

    # 入力値（枚数）を安全にint化して集める
    detail = {}
    for _, key, _ in bills_coins:
        detail[key] = to_int(request.POST.get(key))

    # 金種別の金額（例：500円×3枚=1500円）を作る
    denoms = []
    for label, key, unit in bills_coins:
        count = detail[key]
        amount = unit * count
        denoms.append({
            "label": label,
            "count": count,
            "unit": unit,
            "amount": amount,
        })

    total = sum(d["amount"] for d in denoms)

    # セッション保存（保持用）
    request.session["regi2_total"] = total
    request.session["regi2_detail"] = detail
    request.session["regi2_denoms"] = denoms  # ←（任意）あとで一覧表示に使える

    return render(request, "register/regi2_result.html", {
        "total": total,
        "denoms": denoms,  # ← テンプレで一覧表示できる
    })



# ----------------------
# 現金合算
# ----------------------

def cash_total(request):
    if not auth_check(request):
        return redirect("/")

    regi1 = request.session.get("regi1_total", 0)
    regi2 = request.session.get("regi2_total", 0)

    total_cash = regi1 + regi2
    request.session["total_cash"] = total_cash

    return render(request, "register/cash_total.html", {
        "regi1": regi1,
        "regi2": regi2,
        "total_cash": total_cash
    })


# ----------------------
# 税込み取引高
# ----------------------

def sales_input(request):
    if not auth_check(request):
        return redirect("/")
    return render(request, "register/sales_input.html")


def sales_result(request):
    if not auth_check(request):
        return redirect("/")

    s1 = to_int(request.POST.get("taxed_sales1"))
    s2 = to_int(request.POST.get("taxed_sales2"))

    taxed_sales = s1 + s2
    request.session["taxed_sales"] = taxed_sales

    return render(request, "register/sales_result.html",
                  {"s1": s1, "s2": s2, "taxed_sales": taxed_sales})


# ----------------------
# ミスレ
# ----------------------

def miss_input(request):
    if not auth_check(request):
        return redirect("/")
    return render(request, "register/miss_input.html")


def miss_result(request):
    if not auth_check(request):
        return redirect("/")

    miss_list = [to_int(m) for m in request.POST.getlist("miss[]")]
    miss_total = sum(miss_list)

    taxed_sales = request.session.get("taxed_sales", 0)
    final_taxed_sales = taxed_sales - miss_total

    request.session["miss_total"] = miss_total
    request.session["final_taxed_sales"] = final_taxed_sales

    return render(request, "register/miss_result.html", {
        "miss_total": miss_total,
        "taxed_sales": taxed_sales,
        "final_taxed_sales": final_taxed_sales
    })


# ----------------------
# 商品券・株主優待・クレジット・MD・釣銭
# ----------------------

def gift_input(request):
    if not auth_check(request):
        return redirect("/")

    if request.method == "POST":
        request.session["gift"] = to_int(request.POST.get("gift"))
        return redirect("/shareholder/")
    return render(request, "register/gift_input.html")


def shareholder_input(request):
    if not auth_check(request):
        return redirect("/")

    if request.method == "POST":
        request.session["shareholder"] = to_int(request.POST.get("shareholder"))
        return redirect("/credit/")
    return render(request, "register/shareholder_input.html")


def credit_input(request):
    if not auth_check(request):
        return redirect("/")
    return render(request, "register/credit_input.html")


def credit_result(request):
    if not auth_check(request):
        return redirect("/")

    credit_total = sum([to_int(c) for c in request.POST.getlist("credit[]")])
    request.session["credit_emoney"] = credit_total

    return render(request, "register/credit_result.html",
                  {"credit_total": credit_total})


def md_input(request):
    if not auth_check(request):
        return redirect("/")

    if request.method == "POST":
        request.session["md_charge"] = to_int(request.POST.get("md"))
        return redirect("/change/")
    return render(request, "register/md_input.html")


def change_input(request):
    if not auth_check(request):
        return redirect("/")

    if request.method == "POST":
        request.session["change_money"] = to_int(request.POST.get("change"))
        return redirect("/summary/")
    return render(request, "register/change_input.html")


# ----------------------
# サマリー
# ----------------------

def summary_view(request):
    if not auth_check(request):
        return redirect("/")
    return render(request, "register/summary.html",
                  dict(request.session))


# ----------------------
# 最終結果
# ----------------------

def final_result(request):
    if not auth_check(request):
        return redirect("/")

    total_cash = request.session.get("total_cash", 0)
    change_money = request.session.get("change_money", 0)
    gift = request.session.get("gift", 0)
    shareholder = request.session.get("shareholder", 0)
    credit = request.session.get("credit_emoney", 0)
    md = request.session.get("md_charge", 0)

    final_taxed_sales = request.session.get("final_taxed_sales", 0)

    final_total_cash = total_cash - change_money
    final_register = final_total_cash + gift + shareholder + credit - md
    difference = final_taxed_sales - final_register

    return render(request, "register/final.html", {
        "final_taxed_sales": final_taxed_sales,
        "final_register": final_register,
        "difference": difference
    })
