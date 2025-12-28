from collections import deque
import bisect

class Order:
    __slots__ = ("id","side","price","qty")
    def __init__(self,i,s,p,q):
        self.id=i; self.side=s; self.price=p; self.qty=q

class OrderBook:
    def __init__(self):
        self.bids={}
        self.asks={}
        self.bid_prices=[]
        self.ask_prices=[]
        self.orders={}
        self.oid=0

    def _insert_bid_price(self,p):
        i=bisect.bisect_left([-x for x in self.bid_prices],-p)
        self.bid_prices.insert(i,p)

    def _insert_ask_price(self,p):
        bisect.insort(self.ask_prices,p)

    def _remove_price(self,side,p):
        if side=="B":
            self.bid_prices.remove(p)
            del self.bids[p]
        else:
            self.ask_prices.remove(p)
            del self.asks[p]

    def add_limit(self,side,price,qty):
        self.oid+=1
        o=Order(self.oid,side,price,qty)
        self.orders[o.id]=o
        book=self.bids if side=="B" else self.asks
        if price not in book:
            book[price]=deque()
            if side=="B": self._insert_bid_price(price)
            else: self._insert_ask_price(price)
        book[price].append(o)
        self._match()
        return o.id

    def add_market(self,side,qty):
        while qty>0:
            if side=="B":
                if not self.ask_prices: break
                p=self.ask_prices[0]
                q=self.asks[p][0]
            else:
                if not self.bid_prices: break
                p=self.bid_prices[0]
                q=self.bids[p][0]
            t=min(qty,q.qty)
            qty-=t
            q.qty-=t
            if q.qty==0:
                self.orders.pop(q.id,None)
                if side=="B":
                    self.asks[p].popleft()
                    if not self.asks[p]: self._remove_price("S",p)
                else:
                    self.bids[p].popleft()
                    if not self.bids[p]: self._remove_price("B",p)

    def cancel(self,order_id):
        o=self.orders.pop(order_id,None)
        if not o: return False
        book=self.bids if o.side=="B" else self.asks
        dq=book[o.price]
        for i,x in enumerate(dq):
            if x.id==order_id:
                dq.remove(x)
                break
        if not dq:
            if o.side=="B": self._remove_price("B",o.price)
            else: self._remove_price("S",o.price)
        return True

    def modify(self,order_id,new_qty):
        o=self.orders.get(order_id)
        if not o: return False
        if new_qty<=0:
            return self.cancel(order_id)
        o.qty=new_qty
        return True

    def _match(self):
        while self.bid_prices and self.ask_prices:
            bp=self.bid_prices[0]
            ap=self.ask_prices[0]
            if bp<ap: break
            b=self.bids[bp][0]
            a=self.asks[ap][0]
            t=min(b.qty,a.qty)
            b.qty-=t
            a.qty-=t
            if b.qty==0:
                self.orders.pop(b.id,None)
                self.bids[bp].popleft()
                if not self.bids[bp]: self._remove_price("B",bp)
            if a.qty==0:
                self.orders.pop(a.id,None)
                self.asks[ap].popleft()
                if not self.asks[ap]: self._remove_price("S",ap)

    def print_book(self,depth=5):
        print("\nASKS")
        for p in self.ask_prices[:depth]:
            print(p,sum(o.qty for o in self.asks[p]))
        print("BIDS")
        for p in self.bid_prices[:depth]:
            print(p,sum(o.qty for o in self.bids[p]))

ob=OrderBook()

orders=[
("L","B",100,10),("L","B",101,5),("L","S",105,7),("L","S",104,3),
("L","B",102,4),("L","S",103,6),("M","B",None,5),("M","S",None,4),
("L","B",101,8),("L","S",102,2),("M","B",None,6),("L","S",106,9),
("L","B",99,12),("M","S",None,10),("L","B",103,1),("L","S",101,5),
("M","B",None,7),("L","B",104,6),("L","S",100,4),("M","S",None,3)
]

for o in orders:
    if o[0]=="L":
        ob.add_limit(o[1],o[2],o[3])
    else:
        ob.add_market(o[1],o[3])
    ob.print_book()

