import cv2
import numpy as np
import heapq
import sys

class Piece:
    def __init__(self, img, id) :
        self.img = img
        self.id = id

        self.grads = [
            img[0,:] - img[1,:], #上
            img[:,0] - img[:,1], #左
            img[-1,:] - img[-2,:],#下
            img[:,-1] - img[:,-2] #右
        ]

        self.edges = [
            img[0,:], #上
            img[:,0], #左
            img[-1,:],#下
            img[:,-1] #右
        ]

    def rotate(self, r): #反時計回りにimgを90*r[deg]回転
        self.img = np.rot90(self.img, r)

    def c_rotate(self, r):
        return np.rot90(self.img, r)

class Forest:
    def __init__(self, id):
        self.root = id
        self.members = [id]
        self.positions = {id: (0,0)}
        self.rotations = {id: 0}
        return

    #木の向き，位置の変更
    def set_position(self, root, x, y, r):
        self.rotate(r)
        self.set_root(root)
        self.parallel_shift(x,y)
        return

    #木の結合
    def union(self, pi, pi_edge, pj, pj_edge, forest):
        real_pi_edge = (pi_edge + self.rotations[pi])%4
        pj_P = self.positions[pi]
        if real_pi_edge==0:
            pj_P = (pj_P[0], pj_P[1]-1)
        elif real_pi_edge==1:
            pj_P = (pj_P[0]-1, pj_P[1])
        elif real_pi_edge==2:
            pj_P = (pj_P[0], pj_P[1]+1)
        elif real_pi_edge==3:
            pj_P = (pj_P[0]+1, pj_P[1])

        r = ((pi_edge + self.rotations[pi])%4 - (pj_edge + forest.rotations[pj])%4 + 2)%4
        forest.set_position(pj, pj_P[0], pj_P[1], r)

        ideal_member_length = len(self.members + forest.members)
        real_member_length = len(set(list(self.positions.values()) + list(forest.positions.values())))
        if (ideal_member_length > real_member_length):
            return self, -1, []

        self.members += forest.members
        self.positions.update(forest.positions)
        self.rotations.update(forest.rotations)

        return self, self.root, self.members

    #回転数の保存
    def save_rotations(self, path):
        rot=""
        minX=minY=256
        maxX=maxY=-256
        for x,y in self.positions.values():
            minX = min(minX, x)
            minY = min(minY, y)
            maxX = max(maxX, x)
            maxY = max(maxY, y)
        l = [[0 for j in range(minX, maxX+1)] for i in range(minY, maxY+1)]
        for id in self.members:
            x,y = self.positions[id]
            x-=minX
            y-=minY
            l[y][x] = (4-self.rotations[id])%4
        for y in range(maxY - minY + 1):
            for x in range(maxX - minX + 1):
                rot += f"{l[y][x]}"
        with open(path, 'w') as f:
            f.write(rot)

    #位置の保存
    def save_positions(self, path):
        pos = ""
        minX=minY=256
        maxX=maxY=-256
        for x,y in self.positions.values():
            minX = min(minX, x)
            minY = min(minY, y)
            maxX = max(maxX, x)
            maxY = max(maxY, y)
        l = [[-1 for j in range(minX, maxX+1)] for i in range(minY, maxY+1)]
        for id in self.members:
            x,y = self.positions[id]
            x-=minX
            y-=minY
            destination = y*(maxX - minX + 1)+x
            l[id//(maxX - minX + 1)][id%(maxX - minX + 1)] = destination
        for y in range(maxY - minY + 1):
            for x in range(maxX - minX):
                pos += f"{l[y][x]} "
            pos += f"{l[y][maxX - minX]}\n"
        with open(path, 'w') as f:
            f.write(pos)
        return (maxX - minX + 1, maxY - minY + 1)

    #別のフォーマットで回転数保存
    def alt_save_rotations(self, path):
        alt_rotations = self.rotations
        r = self.rotations[0]
        for id in self.members:
            alt_rotations[id] = (self.rotations[id] - r)%4
        with open(path, 'w') as f:
            f.write(str(alt_rotations))

    #別のフォーマットで位置保存
    def alt_save_positions(self, path):
        with open(path, 'w') as f:
            f.write(str(self.positions))

    #木の回転
    def rotate(self, r): #r : 反時計回り回転数
        for id in self.members:
            x,y = self.positions[id]
            self.rotations[id] = (self.rotations[id] + r)%4
            if r==1:
                self.positions[id] = (y,-x)
            if r==2:
                self.positions[id] = (-x,-y)
            if r==3:
                self.positions[id] = (-y,x)
        return

    #根の更新
    def set_root(self, rn): #rn : 新しい根
        xn,yn = self.positions[rn]
        self.root = rn
        self.parallel_shift(-xn, -yn)
        return

    #木の平行移動
    def parallel_shift(self, dx, dy):
        for id in self.members:
            self.positions[id] = (self.positions[id][0] + dx, self.positions[id][1] + dy)
        return

class Solver:
    def __init__(self, col, row, pieces, size):
        self.col = col
        self.row = row
        self.piece_num = col * row
        self.pieces = pieces
        self.size = size

        self.queue = []
        self.parents = [id for id in range(col*row)]
        self.forests = [Forest(id) for id in range(col*row)]

        self.culc_match()
        return

    #ピース間の類似度計算
    def culc_match(self):
        for i in range(self.piece_num):
            for j in range(i+1, self.piece_num):
                for i_dir in range(4):
                    for j_dir in range(4):
                        diff = self.calc_diff(i, i_dir, j, j_dir)
                        if diff<1:
                            continue
                        heapq.heappush(
                            self.queue,
                            (diff, i, i_dir, j, j_dir)
                    )
        return

    #復元関数
    def run(self):
        while(len(self.queue)):
            diff, pi, pi_edge, pj, pj_edge = heapq.heappop(self.queue)
            if(self.parents[pi] == self.parents[pj]): continue
            forest, forest_root, forest_member = self.forests[self.parents[pi]].union(pi, pi_edge, pj, pj_edge, self.forests[self.parents[pj]])
            if forest_root == -1: continue
            for id in forest_member:
                self.parents[id] = forest_root
                self.forests[id] = 0
            self.forests[forest_root] = forest
            print(f"union: {pi} edge{pi_edge} ### {pj} edge{pj_edge}")
            if len(set(self.parents)) == 1: break
        for forest in self.forests:
            if forest == 0: continue
            forest.rotate((4-forest.rotations[0])%4) #復元前画像の左上ピースに回転を合わせる
            self.create_img(forest)
            w, h = forest.save_positions("pos.txt")
            forest.save_rotations("rot.txt")
            forest.alt_save_positions("alt_pos.txt")
            forest.alt_save_rotations("alt_rot.txt")
            print("complete fixing")
        return w,h

    #ピース間類似度計算
    def calc_diff(self, i, i_dir, j, j_dir):
        i_edge = self.pieces[i].edges[i_dir]
        j_edge = self.pieces[j].edges[j_dir]

        i_grad = self.pieces[i].grads[i_dir]
        j_grad = self.pieces[j].grads[j_dir]
        #辺の向きを合わせる
        if (i_dir in [0, 3]) == (j_dir in [0, 3]):
            j_edge = j_edge[::-1]
            j_grad = j_grad[::-1]
        p = 3/10
        q = 1/16
        pred1 = np.power(np.linalg.norm(i_grad - j_edge + i_edge), p)
        pred2 = np.power(np.linalg.norm(j_grad - i_edge + j_edge), p)
        return (pred1 + pred2) ** (q/p)

    #ndarrayを画像変換
    def create_img(self, forest):
        minX=minY=256
        maxX=maxY=-256
        for x,y in forest.positions.values():
            minX = min(minX, x)
            minY = min(minY, y)
            maxX = max(maxX, x)
            maxY = max(maxY, y)
        pic = np.zeros(((maxY-minY+1)*self.size, (maxX-minX+1)*self.size, 3))
        for id, pos in forest.positions.items():
            self.pieces[id].rotate(forest.rotations[id])
            pic[(pos[1]-minY)*self.size:(pos[1]-minY+1)*self.size, (pos[0]-minX)*self.size:(pos[0]-minX+1)*self.size] = self.pieces[id].img
        cv2.imwrite("fix.png", pic)

#ピースの分割数，ピースサイズの保存
def save_size(path, size, cols, rows):
    with open(path, 'w') as f:
        f.write(f'{rows}, {cols}, {size}')

if __name__ == "__main__":
    FILE = sys.argv[1]
    img = cv2.imread(FILE)

    cv2.imwrite("problem.png", img)

    col = int(sys.argv[2])
    row = int(sys.argv[3])
    PIECE_SIZE = img.shape[0] // col
    print(col, row)
    pieces = [Piece(part, i) for i, part in enumerate(np.reshape([np.hsplit(h, row) for h in np.vsplit(img.astype(np.int16), col)], (-1, PIECE_SIZE, PIECE_SIZE, 3)))]
    Solver(col, row, pieces, PIECE_SIZE).run()

    save_size("size.txt", PIECE_SIZE, col, row)

def solve(col, row):
    img = cv2.imread("problem.ppm")

    cv2.imwrite("problem.png", img)

    PIECE_SIZE = img.shape[0] // col
    pieces = [Piece(part, i) for i, part in enumerate(np.reshape([np.hsplit(h, row) for h in np.vsplit(img.astype(np.int16), col)], (-1, PIECE_SIZE, PIECE_SIZE, 3)))]
    w, h = Solver(col, row, pieces, PIECE_SIZE).run()

    save_size("size.txt", PIECE_SIZE, col, row)
    if w==row and h==col:
        print("We win")
        return 1
    else:
        print("Need Human Power")
        return 0