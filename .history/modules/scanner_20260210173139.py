#!/usr/bin/env python3
"""软件版本扫描模块"""

import os
import re
import subps
efversionns:
        dict: 软件名称 -> {版本号 -> 安装路径}
    """
    software_versions = {}
    
    # 扫描常见软件
    software_versions.update(scan_python_versions())
    software_versions.update(scan_node_versions())
    software_versions.update(scan_java_versions())
    software_versions.update(scan_git_versions())
    
    return software_versions


def find_executable(name):
    """查找可执行文件路径
    
    Args:
        name (str): 可执行文件名称
    
    Returns:
        list: 可执行文件路径列表
    """
    paths = []
    
    # 从系统PATH环境变量中查找
    path_env = os.environ.get('PATH', '')
    for path in path_env.split(';'):
        if path.strip():
            exe_path = os.path.join(path, name)
            if os.path.exists(exe_path):
                paths.append(exe_path)
            # 检查带.exe扩展名的版本
            exe_path_exe = f"{exe_path}.exe"
            if os.path.exists(exe_path_exe):
                paths.append(exe_path_exe)
    
    # 去重并返回
    return list(set(paths))


def scan_python_versions():
    """扫描Python版本"""
    versions = {}
  s tr_pyth# _v使o_uontpa pytho"""扫描Pyhi 版本 获取Pythonv r  onpoce{}s.run(, "--vt  :ure_output#=使用Py h  的方式查找Py hon可执行文件xt=True,
 y ho _ a_hD = f  l_uxecu abl  "pc\+oi"terr)
    
         fo iv th    py  p_pa h :pt:
         ifocea"h.txihso a h:    versions = yth#o获取Pyt.件 版本= find_exeablenode_ays:      o.h.exists(patv r  o _   ult_=rsubp = sb
tui(         captr
      texe[ ath, "--v r   n"], retiopoE_O     )
     _nod  
u r_=ept 
eT u , ur:vref sn_jaaons( vers{ #x使=Tyu        javand_execujava")
creati  flags=s bprocfss.hs:
           h.ts(p          # 获取Ja      try:   vion_sult = v    o _  tule.   utec,   == 0:    crtionlbpros          v
   o  manchco  _.mchrch(r"Pa*hoe (\r+\o\d+\.\e+)"  v  vi   vesu_ .s  sin              excep        if vesion_m tch:  except:
   ss
    
    reveusionJ=avrosid_maschggrvoi(1"
    rsio}
# 使用的式path= fidablvtr"
o s[v  si  ]=
 at
     #取Git本       ex e  :.run(         t,     eass       u,   :          aI        turnco0:
   {"Py h n": v  s ens}tch = re.searchnide version (\d+\.\d+\.\d+N"de.js version_result.stdout)
                        if version_matchN de.js               n de    version = version_matcnodep(1)
                            nidens[version] = path
                except:
                    paN de.js  except:
        pass
    
    return {"Giverti n_resvles= ibposs.
                        ,    captu_oupt=Tu,txTrue,
                       ciflags=ubpocess.CREATE_NO_WINDOW                )
result.reurnode == 0resulstdt.strip().lstri'v'Nde.jsjavaJavaJavajavajavajavaJava_sltubprceunpath, "-",au_oupt=Tu,tex=True,ceoflg=ubroc.CREATE_NO_WINDOW)if_result.version_result.verin_resl =bpcss.
                        , 
                        capture_output=True, 
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    version_result.version_result.