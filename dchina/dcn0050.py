"""
This is a program to draw map of China-DEM.
Copyright  2020.
Developed by Haolisheng on 2020.2.28.
"""
import numpy as np
import matplotlib.pyplot as plt
import struct
import maskout1
from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap  # import Basemap
from matplotlib.font_manager import FontProperties
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
font = FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf')

#创建三个列表用于存放点的数据
x=[]
y=[] 
z=[]
nx=1400
ny=1200
dxy=0.05
with open(r'./china005.grd','rb') as f:
    for j in range(ny):
        for i in range(nx):
            lon0=70+i*dxy+dxy/2.0
            lat0= 0+j*dxy+dxy/2.0            
            data0=f.read(4)         #ur每次读4个字节 
            z0=struct.unpack('f',data0)[0]
            if z0==-999000000.0:
                z0=-1.0
            x.append(float(lon0))            
            y.append(float(lat0))             
            z.append(float(z0))
xi=np.linspace(min(x),max(x),nx)
yi=np.linspace(min(y),max(y),ny)
xi,yi=np.meshgrid(xi,yi)                                #网格化
zi=griddata((x,y),z,(xi,yi),method='linear')                  #去掉缺省值-1

fig = plt.figure(figsize=(12,9))
ax = fig.add_subplot(111)
lon1 = 72
lon2 = 136
lat1 =15
lat2 = 55
map=Basemap(llcrnrlon=lon1,llcrnrlat=lat1,urcrnrlon=lon2,urcrnrlat=lat2,resolution='l')
map.readshapefile(r'./china1','whatevername',color='k',linewidth=0.3)
map.readshapefile(r'./river1','whatevername',color='black',linewidth=0.5)
# map.drawmapboundary(fill_color='lightblue')
c12 = plt.contourf(xi,yi,zi,range(-200,8500,100),cmap= 'terrain')
clip=maskout1.shp2clip(c12,ax,r'./china0')

plt.rcParams['font.family'] = 'DejaVu Sans'   #设置colorbar的label字体
plt.rcParams['font.size'] = 16                 #设置colorbar的label字体大小
# bar=plt.colorbar(c12,orientation='horizontal', shrink=0.9,aspect=35,fraction=.04, pad=0.055)  #aspect控制bar宽度，fraction控制大小比例,pad控制位置
# bar.ax.tick_params(labelsize=10)           #设置colorbar刻度字体大小。
# bar.set_ticks(range(0,7000,1000))            #设置colorbar刻度标记间隔

# plt.title(u'中国地形高度',fontproperties=font,fontsize=14)

map.drawparallels(
    np.arange(-90, 90.1, 10.),    # 画纬度，范围为[-90,90]间隔为30
    color = 'black',
    # dashes=[5,5],
    fontsize= 10,
    linewidth = 0.1,
    labels=[True, False, False, False]   # labels = [left,right,top,bottom]
    )
map.drawmeridians(
    np.arange(0, 360, 10.),     # 画纬度，范围为[-180,180]间隔为60
    color = 'black',
    # dashes=[5,5],
    fontsize= 10,
    linewidth = 0.1,
    labels=[False, False, False, True]   # labels = [left,right,top,bottom]
    )

#以下截取南海区域
# sub_ax = fig.add_axes([0.773, 0.197, 0.144, 0.18])    #[*left*, *bottom*, *width*,*height*]
sub_ax = fig.add_axes([0.773,0.173, 0.144, 0.18])    #[*left*, *bottom*, *width*,*height*]
lon1 = 105
lon2 = 125
lat1 =0
lat2 = 25
map=Basemap(llcrnrlon=lon1,llcrnrlat=lat1,urcrnrlon=lon2,urcrnrlat=lat2,projection = 'cyl',resolution='l')
map.readshapefile(r'./china1','whatevername',color='black',linewidth=0.5)
# map.drawmapboundary(fill_color='lightblue')
c22 = sub_ax.contourf(xi,yi,zi,range(-100,8500,100),cmap= 'terrain')
clip=maskout1.shp2clip(c22,sub_ax,r'./China0') 

plt.savefig(r'dcn005.jpg',dpi=300,bbox_inches='tight')   #把得到的图保存为png或pdf的格式
plt.show()


