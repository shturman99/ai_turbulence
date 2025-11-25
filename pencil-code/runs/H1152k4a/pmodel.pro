;$Id: pmodel.pro,v 1.3 2024/05/02 03:51:00 brandenb Exp $
if !d.name eq 'PS' then begin
  thick=1.5
  device,xsize=18,ysize=7,yoffset=3
  !p.charthick=thick & !p.thick=thick & !x.thick=thick & !y.thick=thick
end
;
@parameters
iit=[0,2,8,24,70]
default,iread,0
default,ihydro,0
default,fourthird,1.
if iread eq 0 then begin
  if ihydro eq 0 then begin
    power,'_kin','_mag',k=k,spec1=spec1,spec2=spec2,i=n,tt=t,/noplot & print,n
  endif else begin
    power,'_kin','hel_kin',k=k,spec1=spec1,spec2=spec2,i=n,tt=t,/noplot & print,n
    ;power,'hel_mag','_mag',k=k,spec1=spec1,spec2=spec2,i=n,tt=t,/noplot & print,n
  endelse
  iread=1
endif
;
siz=1.4
!p.multi=0
!x.title='!8k!6/!8k!6!d0!n'
!y.title='!8E!6!dM!n!6(!8k,t!6)'
!x.margin=[7.0,.3]
!y.margin=[3.2,.3]
!p.charsize=siz
!p.multi=[0,2,1]
tilde='!9!s!aA!n!r!6'
;
default,w,.1
default,k0,60.
default,vA0,1.
s0=1e4
s=s0/(vA0^2*k0)
yr=[5e-8,5e0]
xr1=[0.01,15.]
xr2=[0.002,2.]
tauA=1./(k0*vA0)
tau=1./(k0*urms0)
print,'tauA,tau=',tauA,tau
pc_read_param,/param2,o=param
nu=param.nu
E=t
EK=t
D=t
II=t
IIK=t
;
plot_oo,k/k0,s*spec2(*,0),xr=xr1,yr=yr,/nodata,xtickf='logticks_exp'
;
nit=n_elements(iit)
for i=0,nit-1 do begin
  it=iit(i)
  oplot,k/k0,s*spec2(*,it)
  Rm=sqrt(2.*mean(spec2(*,it)))/(nu*k0)
  print,it,t(it)/tauA
  wait,w
endfor
xx=[.03,.23] & oplot,xx,xx^4,col=122
xx=[.08,1.7] & oplot,xx,1e-3/xx^2,col=55
xyouts,.08,1e-5,siz=siz,'!8k!6!u4!n',col=122
xyouts,.5,1e-4,siz=siz,'!8k!6!u-2!n',col=55
xyouts,6.,.8,siz=siz,'!6(a)'
;
;  compare with model
;
!y.title='!6'
dir='~/pde/1D/inv_casc_model_tau/' & file='tmp'
dir='~/pde/1D/inv_casc_model/' & file='model'
restore,dir+file+'.sav'
nt=n_elements(tt)
plot_oo,k,EEE[*,0],xr=xr2,yr=yr,xtickf='logticks_exp'
xyouts,.9,.8,siz=siz,'!6(b)'
;
it1=2
print,nt
HHM=fltarr(nt)
EEM=fltarr(nt)
xiM=fltarr(nt)
for it=it1,nt-1 do begin
  oplot,k,EEE[*,it]
  HHM[it]=total(k*HHH[*,it])
  EEM[it]=total(k*EEE[*,it])
  xiM[it]=total(EEE[*,it])/EEM[it]
  print,tt[it],EEM[it],1./xiM[it],HHM[it]
  ;oplot,[1,1]/xiM,yr,col=188
  ;wait,.2
endfor
;
xx=[.04,.10] & oplot,xx,1e11*xx^12,col=122
xx=[.45,.8] & oplot,xx,1e-7/xx^20,col=55
;
qq=+deriv(alog(tt),alog(xiM))
pp=-deriv(alog(tt),alog(EEM))
;
print,"$mv idl.ps ~/tex/mhd/50yrMFT/fig/pmodel.ps"
print,"$mv idl.ps ~/tex/mhd/kohei/fig/pmodel.ps"
print,"$mv idl.ps ~/tex/mhd/kohei/fig/pmodel_tau.ps"
END
