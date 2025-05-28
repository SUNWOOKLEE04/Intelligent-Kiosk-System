"""
주문 관리 모듈 - 주문 추가/제거, 총액 계산, Excel 저장
"""
import pandas as pd
from config import MENU_DATA
import os

class OrderManager:
    def __init__(self):
        self.orders = {}  # {menu_id: {"single": count, "set": count}}
        self.total_price = 0
        
    def add_item(self, menu_id, item_type="single", quantity=1):
        """메뉴 아이템 추가"""
        if menu_id not in MENU_DATA:
            print(f"잘못된 메뉴 ID: {menu_id}")
            return False
            
        if menu_id not in self.orders:
            self.orders[menu_id] = {"single": 0, "set": 0}
            
        self.orders[menu_id][item_type] += quantity
        
        # 가격 계산
        price_key = f"{item_type}_price"
        self.total_price += MENU_DATA[menu_id][price_key] * quantity
        
        print(f"{MENU_DATA[menu_id]['name']} {item_type} {quantity}개 추가됨")
        return True
        
    def remove_item(self, menu_id, item_type="single", quantity=1):
        """메뉴 아이템 제거"""
        if menu_id in self.orders and self.orders[menu_id][item_type] > 0:
            remove_qty = min(quantity, self.orders[menu_id][item_type])
            self.orders[menu_id][item_type] -= remove_qty
            
            # 가격 차감
            price_key = f"{item_type}_price"
            self.total_price -= MENU_DATA[menu_id][price_key] * remove_qty
            
            print(f"{MENU_DATA[menu_id]['name']} {item_type} {remove_qty}개 제거됨")
            return True
        return False
            
    def get_order_summary(self):
        """주문 요약 반환"""
        summary = []
        for menu_id, counts in self.orders.items():
            if counts["single"] > 0 or counts["set"] > 0:
                menu_name = MENU_DATA[menu_id]["name"]
                summary.append({
                    "menu_id": menu_id,
                    "menu": menu_name,
                    "single_count": counts["single"],
                    "set_count": counts["set"],
                    "single_price": MENU_DATA[menu_id]["single_price"],
                    "set_price": MENU_DATA[menu_id]["set_price"]
                })
        return summary
        
    def get_order_count(self, menu_id, item_type):
        """특정 메뉴의 주문 개수 반환"""
        if menu_id in self.orders:
            return self.orders[menu_id][item_type]
        return 0
        
    def save_to_excel(self, filename="payment_details.xlsx"):
        """주문 내역을 Excel로 저장"""
        summary = self.get_order_summary()
        if not summary:
            print("저장할 주문 내역이 없습니다.")
            return False
            
        try:
            data = []
            for item in summary:
                if item["single_count"] > 0:
                    data.append([
                        item["menu"], 
                        item["single_count"], 
                        item["single_price"], 
                        item["single_count"] * item["single_price"]
                    ])
                if item["set_count"] > 0:
                    data.append([
                        item["menu"] + " 세트", 
                        item["set_count"], 
                        item["set_price"], 
                        item["set_count"] * item["set_price"]
                    ])
                    
            df = pd.DataFrame(data, columns=["메뉴", "수량", "단가", "금액"])
            df.loc[len(df)] = ["총합", "", "", self.total_price]
            df.to_excel(filename, index=False)
            
            print(f"주문 내역이 {filename}에 저장되었습니다.")
            return True
            
        except Exception as e:
            print(f"Excel 저장 오류: {e}")
            return False
        
    def clear_orders(self):
        """주문 초기화"""
        self.orders.clear()
        self.total_price = 0
        print("주문이 초기화되었습니다.")
        
    def is_empty(self):
        """주문이 비어있는지 확인"""
        return self.total_price == 0
