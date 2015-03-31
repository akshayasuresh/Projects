pro movie

th=fltarr(200)
pi=3.14159
openr,f,'thetatest.dat',/get_lun
readf,f,th
close,f

a=30
z=12
x=1/(1+exp(-z*(th-(.79))))
y=1/(1+exp(z*(th-(2.36))))

LOADCT, 12

; video production set-up
nnx1=750  ; width of window
nny1=500
nnx2=2*300  ; width of region of interest
nny2=2*230
nnx3=80 ; offsets to the region of interest
nny3=20 ; offsets to the region of interest
pos1=[0.2,0.2,0.9,0.9]
xr=[0.,1.0]
yr=[0.,1.0]
xlab=-0.3
ylab=1.2
thk=2
chsiz=1.5
ncyc=5.
ccolp=   [30,16,10]
image=bytarr(nnx2,nny2)
window,2,retain=2,xs=nnx1,ys=nny1



for j=30,199,1 do begin
;   plot, th, -1*x*y*sin(-2*th),thick=3.0,linestyle=2,title='Movement
;   of Gaussian Distributions', xrange=[-0.2,3.5]
   if j lt 150 then begin
      w=x*y*sin(-2*(300-j)*pi/300)*exp(-(th-((300-j)*pi/300))^2/0.011)
      plot,th,w,thick=9.0,color=90,title='Movement of Gaussian Distributions', xrange=[-0.2,3.5], yrange=[-1,1]
   endif
   if j ge 150 then begin
      w=-1*x*y*sin(-2*(420-j)*pi/300)*exp(-(th-((420-j)*pi/300))^2/0.011)
      plot,th,w,thick=9.0,color=180,title='Movement of Gaussian Distributions', xrange=[-0.2,3.5], yrange=[-1,1]
   endif
   if j ge 30 AND j le 99 then begin
      z=x*y*sin(-2*j*pi/200)*exp(-(th-(j*pi/200))^2/0.011)
      oplot,th,z,thick=9.0,Color=180
   endif
   if j ge 100 AND j le 199 then begin
      oplot,th,-1*x*y*sin(-2*(j-100)*pi/200)*exp(-(th-((j-100)*pi/200))^2/0.011),thick=9.0,color=90
   endif
   xyouts, -0.1, 0.7, 'Over the 11 year solar cycle, the '
   xyouts, -0.1, 0.6, 'Gaussians in each hemisphere ' 
   xyouts, -0.1,0.5, 'move inwards from 45 deg. to the'
   xyouts, -0.1,0.4, 'equator. Here, the southern'
   xyouts, -0.1,0.3, 'hemisphere lags behind the north.'
   xyouts, 1.4,-0.5, '*Each Gaussian is 10 deg. at FWHM'

   image(*,*)=tvrd(nnx3,nny3,nnx2,nny2)
   write_gif,'testanimat.gif',image, rr,gg,bb,/MULTIPLE

endfor
end
