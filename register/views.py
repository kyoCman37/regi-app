from django.shortcuts import render, redirect

# ----------------------
# 共通
# ----------------------

def to_int(value):
    if value == "" or value is None:
        return 0
    return int(value)

# ----------------------
# START
# ----------------------

def start(request):
    return render(request, "register/start.html")

# ----------------------
# レジ1
# ----------------------

def regi1_input(request):
    data = request.session.get("regi1_detail", {})
    return render(request, "register/regi1_input.html", data)

def regi1_result(request):
    if request.method == "POST":

        yen10000 = to_int(request.POST.get("yen10000"))
        yen5000  = to_int(request.POST.get("yen5000"))
        yen1000  = to_int(request.POST.get("yen1000"))
        yen500   = to_int(request.POST.get("yen500"))
        yen100   = to_int(request.POST.get("yen100"))
        yen50    = to_int(request.POST.get("yen50"))
        yen10    = to_int(request.POST.get("yen10"))
        yen5     = to_int(request.POST.get("yen5"))
        yen1     = to_int(request.POST.get("yen1"))

        total = (
            10000*yen10000 + 5000*yen5000 + 1000*yen1000 +
            500*yen500 + 100*yen100 + 50*yen50 +
            10*yen10 + 5*yen5 + 1*yen1
        )

        request.session["regi1_total"] = total
        request.session["regi1_detail"] = {
            "yen10000": yen10000,
            "yen5000": yen5000,
            "yen1000": yen1000,
            "yen500": yen500,
            "yen100": yen100,
            "yen50": yen50,
            "yen10": yen10,
            "yen5": yen5,
            "yen1": yen1,
        }

        return render(request, "register/regi1_result.html", {"total": total})

# ----------------------
# レジ2
# ----------------------

def regi2_input(request):
    data = request.session.get("regi2_detail", {})
    return render(request, "register/regi2_input.html", data)

def regi2_result(request):
    if request.method == "POST":

        yen10000 = to_int(request.POST.get("yen10000"))
        yen5000  = to_int(request.POST.get("yen5000"))
        yen1000  = to_int(request.POST.get("yen1000"))
        yen500   = to_int(request.POST.get("yen500"))
        yen100   = to_int(request.POST.get("yen100"))
        yen50    = to_int(request.POST.get("yen50"))
        yen10    = to_int(request.POST.get("yen10"))
        yen5     = to_int(request.POST.get("yen5"))
        yen1     = to_int(request.POST.get("yen1"))

        total = (
            10000*yen10000 + 5000*yen5000 + 1000*yen1000 +
            500*yen500 + 100*yen100 + 50*yen50 +
            10*yen10 + 5*yen5 + 1*yen1
        )

        request.session["regi2_total"] = total
        request.session["regi2_detail"] = {
            "yen10000": yen10000,
            "yen5000": yen5000,
            "yen1000": yen1000,
            "yen500": yen500,
            "yen100": yen100,
            "yen50": yen50,
            "yen10": yen10,
            "yen5": yen5,
            "yen1": yen1,
        }

        return render(request, "register/regi2_result.html", {"total": total})

# ----------------------
# 現金合算
# ----------------------

def cash_total(request):
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
    return render(request, "register/sales_input.html", {
        "s1": request.session.get("sales1", 0),
        "s2": request.session.get("sales2", 0),
    })

def sales_result(request):
    s1 = to_int(request.POST.get("taxed_sales1"))
    s2 = to_int(request.POST.get("taxed_sales2"))

    request.session["sales1"] = s1
    request.session["sales2"] = s2

    taxed_sales = s1 + s2
    request.session["taxed_sales"] = taxed_sales

    return render(request, "register/sales_result.html", {
        "s1": s1, "s2": s2, "taxed_sales": taxed_sales
    })

# ----------------------
# ミスレ
# ----------------------

def miss_input(request):
    return render(request, "register/miss_input.html")

def miss_result(request):

    miss_list = request.POST.getlist("miss[]")
    miss_list = [to_int(m) for m in miss_list]

    miss_total = sum(miss_list)

    taxed_sales = request.session.get("taxed_sales", 0)
    final_taxed_sales = taxed_sales - miss_total

    request.session["miss_total"] = miss_total
    request.session["final_taxed_sales"] = final_taxed_sales

    return render(request, "register/miss_result.html", {
        "miss_total": miss_total,
        "taxed_sales": taxed_sales,          # ← 追加
        "final_taxed_sales": final_taxed_sales
    })

    miss_list = request.POST.getlist("miss[]")
    miss_list = [to_int(m) for m in miss_list]

    miss_total = sum(miss_list)
    taxed_sales = request.session.get("taxed_sales", 0)
    final_taxed_sales = taxed_sales - miss_total

    request.session["miss_total"] = miss_total
    request.session["final_taxed_sales"] = final_taxed_sales

    return render(request, "register/miss_result.html", {
        "miss_total": miss_total,
        "final_taxed_sales": final_taxed_sales
    })

# ----------------------
# 商品券・株主優待・クレジット・MD・釣銭
# ----------------------

def gift_input(request):
    if request.method == "POST":
        request.session["gift"] = to_int(request.POST.get("gift"))
        return redirect("/shareholder/")
    return render(request, "register/gift_input.html",
                  {"gift": request.session.get("gift", 0)})

def shareholder_input(request):
    if request.method == "POST":
        request.session["shareholder"] = to_int(request.POST.get("shareholder"))
        return redirect("/credit/")
    return render(request, "register/shareholder_input.html",
                  {"shareholder": request.session.get("shareholder", 0)})

def credit_input(request):
    return render(request, "register/credit_input.html")

def credit_result(request):
    credit_list = request.POST.getlist("credit[]")
    credit_list = [to_int(c) for c in credit_list]
    credit_total = sum(credit_list)
    request.session["credit_emoney"] = credit_total

    return render(request, "register/credit_result.html",
                  {"credit_total": credit_total})

def md_input(request):
    if request.method == "POST":
        request.session["md_charge"] = to_int(request.POST.get("md"))
        return redirect("/change/")
    return render(request, "register/md_input.html",
                  {"md": request.session.get("md_charge", 0)})

def change_input(request):
    if request.method == "POST":
        request.session["change_money"] = to_int(request.POST.get("change"))
        return redirect("/summary/")
    return render(request, "register/change_input.html",
                  {"change": request.session.get("change_money", 0)})

# ----------------------
# サマリー
# ----------------------

def summary_view(request):
    return render(request, "register/summary.html", dict(request.session))

# ----------------------
# 最終結果
# ----------------------

def final_result(request):

    total_cash = request.session.get("total_cash", 0)
    change_money = request.session.get("change_money", 0)

    gift = request.session.get("gift", 0)
    shareholder = request.session.get("shareholder", 0)
    credit = request.session.get("credit_emoney", 0)
    md = request.session.get("md_charge", 0)

    final_taxed_sales = request.session.get("final_taxed_sales", 0)

    final_total_cash = total_cash - change_money

    final_register = final_total_cash + gift + shareholder + credit - md
    difference =  final_register - final_taxed_sales

    return render(request, "register/final.html", {
        "final_taxed_sales": final_taxed_sales,
        "final_register": final_register,
        "difference": difference
    })
